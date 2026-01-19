import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from src.sentiment import analyze_sentiment

def render_sentiment_chart(history_data):
    """
    Renders a line chart of sentiment over time.
    """
    if not history_data:
        return None
        
    df = pd.DataFrame(history_data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Create Line Chart
    fig = px.line(
        df, 
        x='timestamp', 
        y='sentiment_score',
        title='Emotional Trajectory',
        markers=True,
        range_y=[-1.1, 1.1],
        labels={'sentiment_score': 'Valence', 'timestamp': 'Time'}
    )
    
    # Add colored regions for visual context
    fig.add_hrect(y0=0.05, y1=1.1, fillcolor="green", opacity=0.1, line_width=0)
    fig.add_hrect(y0=-0.05, y1=0.05, fillcolor="gray", opacity=0.1, line_width=0)
    fig.add_hrect(y0=-1.1, y1=-0.05, fillcolor="red", opacity=0.1, line_width=0)
    
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
    
    return fig

def render_chat_sentiment_trajectory(chat_messages, entry_sentiment_score):
    """
    Renders a sentiment trajectory for a specific chat.
    Tracks emotional changes throughout the conversation.
    """
    if not chat_messages:
        return None
    
    # Analyze sentiment for each user message in the chat
    sentiment_data = []
    message_index = 0
    
    for i, msg in enumerate(chat_messages):
        if msg['role'] == 'user':
            sentiment = analyze_sentiment(msg['message'])
            sentiment_data.append({
                'message_number': message_index + 1,
                'sentiment_score': sentiment['score'],
                'sentiment_label': sentiment['label'],
                'message_type': 'User Input'
            })
            message_index += 1
    
    if not sentiment_data:
        return None
    
    df = pd.DataFrame(sentiment_data)
    
    # Create Line Chart for chat progression
    fig = go.Figure()
    
    # Add line for sentiment progression
    fig.add_trace(go.Scatter(
        x=df['message_number'],
        y=df['sentiment_score'],
        mode='lines+markers',
        name='Emotional State',
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=8)
    ))
    
    # Add the initial entry sentiment as a baseline
    fig.add_hline(
        y=entry_sentiment_score,
        line_dash="dash",
        line_color="gray",
        annotation_text=f"Entry Start: {entry_sentiment_score:.2f}",
        annotation_position="right"
    )
    
    # Add colored regions
    fig.add_hrect(y0=0.05, y1=1.1, fillcolor="green", opacity=0.1, line_width=0)
    fig.add_hrect(y0=-0.05, y1=0.05, fillcolor="gray", opacity=0.1, line_width=0)
    fig.add_hrect(y0=-1.1, y1=-0.05, fillcolor="red", opacity=0.1, line_width=0)
    
    fig.update_layout(
        title='Chat Emotional Trajectory',
        xaxis_title='User Message Number',
        yaxis_title='Emotional Valence',
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        yaxis=dict(range=[-1.1, 1.1]),
        showlegend=True
    )
    
    return fig