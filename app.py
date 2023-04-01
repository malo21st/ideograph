import streamlit
from streamlit_agraph import agraph, Node, Edge, Config

nodes = []
edges = []
nodes.append( Node(id="pref01", 
                   label="東京", 
                   size=25, 
#                    shape="circularImage",
#                    image="http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_spiderman.png"
                  )
            ) # includes **kwargs
nodes.append( Node(id="pref02", 
                   label="福岡", 
                   size=25,
#                    shape="circularImage",
#                    image="http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_captainmarvel.png"
                  )
            )
edges.append( Edge(source="pref01", 
#                    label="friend_of", 
                   target="pref02", 
                   # **kwargs
                   ) 
            ) 
edges.append( Edge(source="pref01", 
#                    label="friend_of", 
                   target="pref01", 
                   # **kwargs
                   ) 
            ) 

config = Config(width=750,
                height=950,
                directed=False, 
                physics=True, 
                hierarchical=False,
                # **kwargs
                )

return_value = agraph(nodes=nodes, 
                      edges=edges, 
                      config=config)
