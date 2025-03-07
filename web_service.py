from flask import Flask, request, send_file, render_template
import os
import torch
import numpy as np
from inference import (
    get_tts_wav,
    change_sovits_weights,
    change_gpt_weights,
    get_weights_names,
    i18n
)
import soundfile as sf
import io

app = Flask(__name__)

# Initialize models
gpt_path = os.environ.get(
    "gpt_path", "pretrained_models/s1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt"
)
sovits_path = os.environ.get("sovits_path", "pretrained_models/s2G488k.pth")

# Load initial models
change_sovits_weights(sovits_path)
change_gpt_weights(gpt_path)

@app.route('/')
def index():
    SoVITS_names, GPT_names = get_weights_names()
    return render_template('index.html', 
                         sovits_models=sorted(SoVITS_names),
                         gpt_models=sorted(GPT_names),
                         languages=[i18n("中文"), i18n("英文"), i18n("日文"), 
                                  i18n("中英混合"), i18n("日英混合"), i18n("多语种混合")],
                         cut_options=[i18n("不切"), i18n("凑四句一切"), i18n("凑50字一切"), 
                                    i18n("按中文句号。切"), i18n("按英文句号.切"), i18n("按标点符号切")])

@app.route('/synthesize', methods=['POST'])
def synthesize():
    try:
        # Get form data
        ref_audio = request.files['reference_audio']
        prompt_text = request.form['prompt_text']
        prompt_language = request.form['prompt_language']
        text = request.form['text']
        text_language = request.form['text_language']
        how_to_cut = request.form['how_to_cut']
        top_k = int(request.form['top_k'])
        top_p = float(request.form['top_p'])
        temperature = float(request.form['temperature'])
        ref_text_free = request.form.get('ref_text_free', 'false').lower() == 'true'

        # Save reference audio temporarily
        temp_audio_path = "temp_reference.wav"
        ref_audio.save(temp_audio_path)

        # Generate audio
        sample_rate, audio_data = next(get_tts_wav(
            temp_audio_path,
            prompt_text,
            prompt_language,
            text,
            text_language,
            how_to_cut,
            top_k,
            top_p,
            temperature,
            ref_text_free
        ))

        # Clean up temp file
        os.remove(temp_audio_path)

        # Convert to WAV format and send
        buffer = io.BytesIO()
        sf.write(buffer, audio_data, sample_rate, format='WAV')
        buffer.seek(0)
        
        return send_file(
            buffer,
            mimetype='audio/wav',
            as_attachment=True,
            download_name='synthesized.wav'
        )

    except Exception as e:
        return str(e), 400

@app.route('/change_model', methods=['POST'])
def change_model():
    try:
        model_type = request.form['type']
        model_path = request.form['path']
        
        if model_type == 'sovits':
            change_sovits_weights(model_path)
        elif model_type == 'gpt':
            change_gpt_weights(model_path)
            
        return "Model changed successfully", 200
    except Exception as e:
        return str(e), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9872, debug=True) 