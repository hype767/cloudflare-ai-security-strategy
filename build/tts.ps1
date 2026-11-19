Add-Type -AssemblyName System.Speech
$out = Join-Path $PSScriptRoot "audio"
New-Item -ItemType Directory -Force $out | Out-Null
$lines = @(
  "AI 시대, 보안의 경계가 사라지고 있습니다.",
  "모든 기업이 AI를 쓰고, 공격자도 AI를 씁니다.",
  "프롬프트 인젝션, 데이터 유출, 섀도 AI. 위협은 이제 모델 안에서 시작됩니다.",
  "육백 개 기업 시뮬레이션 분석 결과, AI 도입 지수가 높은 기업은 사고가 서른 배 많았습니다.",
  "클라우드플레어는 AI 게이트웨이, AI 방화벽, 제로 트러스트로 세 겹의 방어선을 세웁니다.",
  "IT와 금융에서 먼저 이기고, 의료와 제조로 넓힙니다. 진단으로 시작해 플랫폼으로 확장합니다.",
  "AI를 믿고 쓰게 만드는 회사. 클라우드플레어."
)
$i = 0
foreach ($t in $lines) {
  $s = New-Object System.Speech.Synthesis.SpeechSynthesizer
  $s.SelectVoice("Microsoft Heami Desktop")
  $s.Rate = 0
  $s.SetOutputToWaveFile((Join-Path $out ("seg$i.wav")))
  $s.Speak($t)
  $s.Dispose()
  $i++
}
"ok $i"
