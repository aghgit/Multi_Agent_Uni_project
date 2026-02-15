from youtube_search import YoutubeSearch

class YouTubeAgent:
    def execute(self, action, query):
        if action != "search" or not query:
            return []
        try:
            # On demande 20 résultats pour avoir plus de choix
            # On ajoute des mots-clés de filtrage pour la qualité
            search_query = f"{query} english"
            results = YoutubeSearch(search_query, max_results=20).to_dict()
            
            videos = []
            for v in results:
                title = v.get('title', 'Untitled')
                channel = v.get('channel', 'Unknown')
                
                videos.append({
                    "title": title,
                    "channel": channel,
                    "link": f"https://www.youtube.com/watch?v={v.get('id')}",
                    "thumbnail": v.get('thumbnails', [None])[0],
                    "views": v.get('views', 'N/A'),
                    "keywords": f"{title} {channel}".lower() 
                })
            return videos
        except Exception as e:
            print(f"Erreur Agent YouTube: {e}")
            return []