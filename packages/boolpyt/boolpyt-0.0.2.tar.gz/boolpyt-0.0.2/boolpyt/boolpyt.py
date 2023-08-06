import pandas as pd
import plotly.graph_objs as go
import plotly.offline as py

def bool_plot_contor(x, y, z, col_name=None, html_path=''):
  '''
  输入三个列表，返回一个html页面
  '''
  if not col_name:
    col_name = ['转速(r/min)', '扭矩(Nm)', '比油耗(g/kWh)']
  if not html_path:
    filename = 'contour.html'
    
  df = pd.DataFrame([x, y, z]).T
  df.columns = col_name
  fig = px.density_contour(df, x=col_name[0], y=col_name[1], z=col_name[2], histfunc="avg")
  fig.update_traces(contours_coloring="fill", contours_showlabels = True)
  py.plot(
    fig, 
    filename=filename,
    # image='png',           
    ) 