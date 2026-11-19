import json, os
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(H)
eda = json.load(open(os.path.join(R, "data", "eda.json"), encoding="utf-8"))
s = open(os.path.join(H, "site_template.html"), encoding="utf-8").read()
s = (s.replace("__EDA__", json.dumps(eda, ensure_ascii=False)).replace("__R_AI__", str(eda["r_ai_inc"]))
      .replace("__R_MAT__", str(eda["r_mat_inc"])).replace("__HOT__", str(eda["hot_total"]))
      .replace("__SLOPE__", str(eda["slope"][0])))
open(os.path.join(R, "index.html"), "w", encoding="utf-8").write(s)
print("index.html", len(s))
