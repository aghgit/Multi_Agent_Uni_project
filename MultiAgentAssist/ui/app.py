from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.image import AsyncImage
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
import webbrowser

from services.llm_interface import LLMInterface
from brain.orchestrator import Orchestrator

# Config Fenêtre
Window.clearcolor = (0.1, 0.1, 0.1, 1)

class VideoCard(BoxLayout):
    def __init__(self, video_data, ranker_ref, ui_ref, **kwargs):
        super().__init__(orientation='horizontal', size_hint_y=None, height=120, padding=5, spacing=10, **kwargs)
        self.video = video_data
        self.ranker = ranker_ref
        self.ui = ui_ref

        # 1. Miniature
        img_src = video_data.get('thumbnail', '')
        self.image = AsyncImage(source=img_src, size_hint_x=0.3, keep_ratio=True, allow_stretch=True)
        self.add_widget(self.image)

        # 2. Infos (Sans le score brut pour rester propre)
        info_layout = BoxLayout(orientation='vertical', size_hint_x=0.5)
        title = Label(
            text=f"[b]{video_data['title']}[/b]", 
            markup=True, halign='left', valign='top', 
            text_size=(350, None), color=(1, 1, 1, 1)
        )
        channel = Label(
            text=f"[color=888888]{video_data['channel']}[/color]", 
            markup=True, halign='left', valign='middle', 
            text_size=(350, None)
        )
        info_layout.add_widget(title)
        info_layout.add_widget(channel)
        self.add_widget(info_layout)

        # 3. Actions
        actions_layout = BoxLayout(orientation='vertical', size_hint_x=0.2, spacing=2)
        
        btn_play = Button(text="PLAY", background_color=(0, 0.7, 1, 1))
        btn_play.bind(on_release=self.on_play)
        
        btn_like = Button(text="LIKE", background_color=(0, 0.8, 0, 1))
        btn_like.bind(on_release=self.on_like)

        btn_dislike = Button(text="DISLIKE", background_color=(0.8, 0, 0, 1))
        btn_dislike.bind(on_release=self.on_dislike)

        actions_layout.add_widget(btn_play)
        actions_layout.add_widget(btn_like)
        actions_layout.add_widget(btn_dislike)
        self.add_widget(actions_layout)

    def on_play(self, instance):
        webbrowser.open(self.video['link'])
        self.ui.add_message("System", f"Lancement de : {self.video['title']}")

    def on_like(self, instance):
        self.ranker.learn_feedback(self.video, "like")
        self.ui.add_message("System", f"Recommandations mises à jour pour {self.video['channel']}")
        instance.disabled = True
        instance.text = "LIKED"

    def on_dislike(self, instance):
        self.ranker.learn_feedback(self.video, "dislike")
        self.ui.add_message("System", f"Chaîne dislike : {self.video['channel']}")
        self.parent.remove_widget(self)

class MainUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=15, spacing=15, **kwargs)
        self.orchestrator = Orchestrator()
        self.llm = LLMInterface()

        self.scroll = ScrollView()
        self.chat_history = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.chat_history.bind(minimum_height=self.chat_history.setter('height'))
        self.scroll.add_widget(self.chat_history)
        self.add_widget(self.scroll)

        self.input_field = TextInput(size_hint_y=None, height=50, multiline=False, hint_text="Tapez votre commande...")
        self.input_field.bind(on_text_validate=self.send_command)
        self.add_widget(self.input_field)

    def add_message(self, role, text):
        safe_text = str(text).replace('[', '&[').replace(']', '&]')
        color = "33CCFF" if role == "You" else "FFCC33"
        if role == "System": color = "AAAAAA"
        
        lbl = Label(
            text=f"[b][color={color}]{role}:[/color][/b] {safe_text}", 
            markup=True, size_hint_y=None, height=40, halign="left", valign="middle"
        )
        lbl.bind(size=lbl.setter('text_size')) 
        self.chat_history.add_widget(lbl)

    def send_command(self, instance):
        user_input = instance.text
        if not user_input: return
        
        self.add_message("You", user_input)
        instance.text = ""
        
        intent = self.llm.process_input(user_input)
        response = self.orchestrator.handle(intent)
        
        if response.get("type") == "video_list":
            res_data = response.get("data")
            if not res_data:
                self.add_message("Assistant", "Aucune vidéo trouvée.")
                return

            self.add_message("Assistant", f"Résultats pour votre recherche :")
            for video in res_data:
                card = VideoCard(video, self.orchestrator.ranker, self)
                self.chat_history.add_widget(card)
        else:
            self.add_message("Assistant", str(response.get("data", "Ok.")))

class AssistantApp(App):
    def build(self):
        return MainUI()

if __name__ == "__main__":
    AssistantApp().run()