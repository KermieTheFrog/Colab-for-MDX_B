# @title Inference
import gradio as gr
from gradio import components
from pathlib import Path
import json
import os
import shutil


with open('model_data.json', 'r') as f:
  model_data = json.load(f)

tracks_path = '/content/drive/MyDrive/MDX_Colab/tracks/'
separated_path = 'separated/'

def process_data(input_path, Denoise, Normalize, Chunks, Shifts):
  track = Path(input_path.name)
  track = track.stem + track.suffix
  shutil.move(input_path.name, tracks_path)
  track = tracks_path+track

  denoise = Denoise
  normalise = Normalize

  amplitude_compensation = model_data["(de)Reverb HQ By FoxJoy"]["compensate"]
  dim_f = model_data["(de)Reverb HQ By FoxJoy"]["mdx_dim_f_set"]
  dim_t = model_data["(de)Reverb HQ By FoxJoy"]["mdx_dim_t_set"]
  n_fft = model_data["(de)Reverb HQ By FoxJoy"]["mdx_n_fft_scale_set"]

  mixing_algorithm = 'min_mag' 
  chunks = Chunks
  shifts = Shifts

  ##validate values
  normalise = '--normalise' if normalise else ''
  denoise = '--denoise' if denoise else ''
  margin = 44100
  os.system(f"python main.py --n_fft {n_fft} --dim_f {dim_f} --dim_t {dim_t} --margin {margin} -i \"{track}\" --mixing {mixing_algorithm} --onnx \"{'onnx/(de)Reverb HQ By FoxJoy'}\" --model off  --shifts {round(shifts)} --stems v --invert v --chunks {chunks} --compensate {amplitude_compensation} {normalise} {denoise}")
  os.remove(track)
  return "De reverb complete!"

input_path = components.File()

Denoise = components.Checkbox(label="Denoise", value=True)
Normalize = components.Checkbox(label="Normalize")
Chunks = components.Slider(label="Chunks", minimum=1, maximum=55, value=55)

Shifts = components.Slider(label="Shifts", minimum=0, maximum=10, value=10)

interface = gr.Interface(
    fn=process_data,
    inputs=[input_path, Denoise, Normalize, Chunks, Shifts],
    outputs="text",
    allow_flagging='never'
)



interface.launch(share = True)
