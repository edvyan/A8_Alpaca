# Import required libraries
import dash
from dash import html, dcc, Output, Input, State
import torch
import pickle

# Load model and tokenizer
model = torch.load('model.pt')
tokenizer = pickle.load(open('tokenizer.pkl', 'rb'))
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Initialize Dash app
app = dash.Dash(__name__)

# Define app layout
app.layout = html.Div([
    dcc.Textarea(id='input-text', style={'width': '100%', 'height': 100}),
    html.Button('Submit', id='submit-val', n_clicks=0),
    html.Div(id='output')
])

# Callback for updating output text
@app.callback(
    Output('output', 'children'),
    Input('submit-val', 'n_clicks'),
    State('input-text', 'value')
)
def update_output(n_clicks, input_text):
    if n_clicks > 0 and input_text is not None:
        input_ids = tokenizer.encode(input_text, return_tensors="pt").to(device)
        output = model.generate(input_ids, max_length=256, num_beams=5, no_repeat_ngram_size=2, top_k=50, top_p=0.95, temperature=0.7)
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        return html.Div(generated_text)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
