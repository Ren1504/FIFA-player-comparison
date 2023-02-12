import streamlit as st
import pandas as pd
import plotly.graph_objects as go


data = pd.read_csv("data.csv",index_col=False)
st.set_page_config(layout = 'wide')

@st.cache

def load_css(f = 'styles.css'):
  with open(f) as f:
    css = f'<style>{f.read()}</style>'
  return css

css = load_css()
st.markdown(css,unsafe_allow_html=True)

st.write("# FIFA PLAYERS COMPARISON")

def overall(idx):
  pace = round((data['Sprint Speed'][idx]*0.55) + (data['Acceleration'][idx]*0.45))

  shoot = round((data['Finishing'][idx]*0.45) + (data['Long Shots'][idx]*0.2) +(data['Shot Power'][idx]*0.2) + (data['Positioning'][idx]*0.05) +(data['Penalties'][idx]*0.05) + (data['Volleys'][idx]*0.05))

  passing = round((data['Short Passing'][idx]*0.35) + (data['Vision'][idx]*0.2) + (data['Crossing'][idx]*0.2) + (data['LongPassing'][idx]*0.15) + (data['Curve'][idx]*0.05) + (data['Freekick Accuracy'][idx]*0.05))

  defend =  round((data['Interceptions'][idx]*0.2) + (data['Heading Accuracy'][idx]*0.1) + (data['Marking'][idx]*0.3) + (data['Sliding Tackle'][idx]*0.1) + (data['Standing Tackle'][idx]*0.3))

  physical = round((data['Aggression'][idx]*0.2) + (data['Jumping'][idx]*0.05) + (data['Stamina'][idx]*0.25) +(data['Strength'][idx]*0.5))

  dribbling = round((data['Agility'][idx]*0.1) + (data['Balance'][idx]*0.05) + (data['Reactions'][idx]*0.05) + (data['Ball Control'][idx]*0.3) + (data['Dribbling'][idx]*0.5))

  return {'Passing': passing,'Dribbling':dribbling,'Pace':pace, 'Physical':physical , 'Defending': defend,'Shooting':shoot}

attack = (data.iloc[0:1,38:43])
gk = (data.iloc[0:1,67:72])


col1,col2,col3 = st.columns(3,gap = "large")


def radar_chart(name,name2,head,val,val2):
  fig = go.Figure()

  fig.add_trace(go.Scatterpolar(
          r = val,
          theta = head,
          fill = 'toself',
          name = name
    ))
  fig.add_trace(go.Scatterpolar(
          r = val2,
          theta = head,
          fill = 'toself',
          name = name2
    ))

  fig.update_layout(
      polar = dict(
        radialaxis = dict(
          visible = False,
          range = [0, 100]
        )),
      showlegend = False
    )

  fig.update_layout(paper_bgcolor = "rgba(0,0,0,0)",
                  plot_bgcolor = "rgba(0,0,0,0)")
  
  st.plotly_chart(fig, use_container_width=True)


with col1:
    name = st.selectbox("Enter name of player",data['Full Name'],key =1 )

    idx = data[data['Full Name'] == name].index.values[0]

    st.image(data['Image Link'][idx].replace("60.png","180.png"))
    st.subheader(name)

    st.subheader(data['Overall'][idx])

    attack = data.iloc[idx:idx+1,38:43]
    attack_head = list(attack.columns)
    attack_val = list(attack.values[0])

    gk = data.iloc[idx:idx+1,67:72]
    gk_head = list(gk.columns)
    gk_val = list(gk.values[0])

    ovr = overall(idx)
    ovr_head = list(ovr.keys())
    ovr_val = list(ovr.values())

    dribble_head = ['Agility','Balance','Reactions','Ball Control','Dribbling']
    dribble_val = [data[i][idx] for i in dribble_head]

    defending_head = ['Interceptions','Heading Accuracy','Marking','Sliding Tackle','Standing Tackle']
    defend_val = [data[j][idx] for j in defending_head]

    st.subheader("Position: "+data['Positions Played'][idx])
    st.subheader("Nationality:"+data['Nationality'][idx])

    if data['Club Position'][idx] == 'GK':
      for i in range(len(gk_val)):
        st.write(gk_head[i],+gk_val[i])
    else:
      for i in range(len(ovr)):
        st.write(ovr_head[i],+ovr_val[i])

  

with col3:
    name2 = st.selectbox("Enter name of player",data['Full Name'],index = 8,key = 2)
    idx2 = data[data['Full Name'] == name2].index.values[0]
    st.image(data['Image Link'][idx2].replace("60.png","180.png"))
    st.subheader(name2)

    st.subheader(data['Overall'][idx2])

    attack2 = data.iloc[idx2:idx2+1,38:43]
    attack_val2 = list(attack2.values[0])

    gk = data.iloc[idx2:idx2+1,67:72]
    gk_val2 = list(gk.values[0])

    ovr2 = overall(idx2)
    ovr_val2 = list(ovr2.values())

    dribble_val2 = [data[i][idx2] for i in dribble_head]

    defend_val2 = [data[j][idx2] for j in defending_head]

    st.subheader("Position: "+data['Positions Played'][idx2])
    st.subheader("Nationality:"+data['Nationality'][idx2])

    if data['Club Position'][idx2] == 'GK':
      for i in range(len(gk_val)):
        st.write(gk_head[i],+gk_val2[i])
    else:
      for i in range(len(ovr)):
        st.write(ovr_head[i],+ovr_val2[i])



with col2:

  st.header("STATS")
  if data['Club Position'][idx2] == 'GK' and data['Club Position'][idx] == 'GK':
       radar_chart(name,name2,gk_head,gk_val,gk_val2)
  st.header("OVERALL")
  radar_chart(name,name2,ovr_head,ovr_val,ovr_val2)
  options = ['ATTACKING','DEFENDING',"DRIBBLING","GOALKEEPING"]
  stat = st.selectbox("Select the stat to compare",options,index = 0,key = 3)
  st.header(stat)
  if stat == 'ATTACKING':
    radar_chart(name,name2,attack_head,attack_val,attack_val2)
  elif stat == 'DEFENDING':
    radar_chart(name,name2,defending_head,defend_val,defend_val2)
  
  elif stat == 'DRIBBLING':
    radar_chart(name,name2,dribble_head,dribble_val,dribble_val2)
  elif stat == 'GOALKEEPING':
    radar_chart(name,name2,gk_head,gk_val,gk_val2)
