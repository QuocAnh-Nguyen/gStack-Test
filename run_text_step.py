import sys
import os
from openai import OpenAI

# Đã thêm tham số <model_name> lên đầu tiên
if len(sys.argv) < 6:
    print("Sử dụng: python run_text_step.py <model_name> <skill_file> <input_files> <output_file> <prompt>")
    sys.exit(1)

model_name = sys.argv[1]
skill_file = sys.argv[2]
input_files_str = sys.argv[3]
output_file = sys.argv[4]
prompt_msg = sys.argv[5]

# Đọc file kỹ năng (SKILL.md)
try:
    with open(skill_file, "r", encoding="utf-8") as f:
        system_prompt = "Act strictly according to the following role and instructions:\n\n" + f.read()
except Exception as e:
    print(f"Lỗi đọc {skill_file}: {e}")
    sys.exit(1)

# Đọc bối cảnh
context = ""
if input_files_str:
    for file_path in input_files_str.split(','):
        file_path = file_path.strip()
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                context += f"\n\n--- NỘI DUNG FILE: {file_path} ---\n\n" + f.read()

full_prompt = f"{context}\n\nUSER REQUEST: {prompt_msg}\n\nPlease output the final requested document in Markdown format."

print(f"🚀 Đang gọi chuyên gia [{skill_file.split('/')[0]}] bằng bộ não [{model_name}]...")

# Gọi API với model được chỉ định
try:
    client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": full_prompt}
        ],
        temperature=0.7
    )
    
    result_text = response.choices[0].message.content
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result_text)
        
    print(f"✅ Đã ghi thành công {len(result_text)} ký tự vào file '{output_file}'!")
except Exception as e:
    print(f"❌ Lỗi khi gọi API: {e}")
