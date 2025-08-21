import osmnx as ox
import folium
import pandas as pd


def plot_route(plot_df): 

  # 1. 지도 중심 계산
  center_lat = plot_df["y"].mean()
  center_lon = plot_df["x"].mean()
  m = folium.Map(location=[center_lat, center_lon], zoom_start=13)

  # 2. osmnx로 도로망 그래프 불러오기 (반경 3km 내 도로망)
  G = ox.graph_from_point((center_lat, center_lon), dist=3000, network_type="drive")

  # 3. 정류장 경로 순서대로 실제 도로 기반 연결
  for i in range(len(plot_df) - 1):
      origin = (plot_df.iloc[i]["y"], plot_df.iloc[i]["x"])
      destination = (plot_df.iloc[i + 1]["y"], plot_df.iloc[i + 1]["x"])
      
      try:
          node_origin = ox.nearest_nodes(G, origin[1], origin[0])
          node_dest = ox.nearest_nodes(G, destination[1], destination[0])
          shortest_path = ox.shortest_path(G, node_origin, node_dest, weight="length")
          path_coords = [(G.nodes[n]["y"], G.nodes[n]["x"]) for n in shortest_path]

          folium.PolyLine(path_coords, color="blue", weight=5, opacity=0.8).add_to(m)
      except Exception as e:
          print(f"🚫 경로 계산 실패 ({plot_df.iloc[i]['정류장_ID']} → {plot_df.iloc[i+1]['정류장_ID']}): {e}")

  # 4. 각 정류장에 마커 추가
  for _, row in plot_df.iterrows():
      folium.Marker(
          location=[row["y"], row["x"]],
          popup=row["정류장_ID"],
          icon=folium.Icon(color="green", icon="info-sign")
      ).add_to(m)
  return m 