---
permalink: /
title: "Practical Speech AI Research and Education"
description: "Speech AI researcher and educator at NAIST building open-source tools (Nkululeko, Speechain), tutorials, and demos in speech processing and multimodal processing."
lang: en
lang_ref: about
author_profile: true
redirect_from:
  - /about/
  - /about.html
---

> Speech AI researcher and educator at NAIST. I build open-source tools,
> tutorials, and demos in speech processing — from speech classification (e.g., emotion recognition) to
> ASR and TTS — to multimodal information fusion.

<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
  mermaid.initialize({ startOnLoad: true, securityLevel: 'loose' });
</script>

<pre class="mermaid">
graph TD
    BTA(((BTA)))

    BTA --> Research["🔬 Research"]
    BTA --> Tools["🛠️ Tools"]
    BTA --> Tutorials["📚 Tutorials"]
    BTA --> Pubs["📄 Publications"]
    BTA --> Contact["📧 Contact"]
    BTA --> More["📁 More"]

    Research --> SER["Speech Emotion Recognition"]
    Research --> MF["Multimodal Fusion"]
    Research --> PV["Pathological Voice"]
    Research --> RT["Research Themes →"]

    Tools --> NK["Nkululeko"]
    Tools --> SA["Speechain"]
    Tools --> PR["PaperRAG"]
    Tools --> GH["All repos on GitHub →"]

    Tutorials --> SL["Shell & Linux"]
    Tutorials --> PY["Python & DSP"]
    Tutorials --> SP["Speech & Audio"]
    Tutorials --> GT["Git & LaTeX"]

    Pubs --> P1["Nkululeko — ICASSP 2026"]
    Pubs --> P2["COVID-19 transfer — IJIT 2025"]
    Pubs --> P3["Dementia from speech — APSIPA 2025"]
    Pubs --> AllP["All publications →"]

    Contact --> Em["Email"]
    Contact --> GHub["github.com/bagustris"]
    Contact --> Sch["Google Scholar"]
    Contact --> CvPage["CV"]

    More --> Crs["Courses"]
    More --> Th["Theses"]
    More --> JA["Japanese Learning"]
    More --> Isl["Islamic Studies"]
    More --> Blg["Blogs"]

    click Research href "/research/" "Research themes"
    click RT href "/research/" "Research themes"
    click Tools href "/tools/" "Tools and Projects"
    click NK href "https://nkululeko.readthedocs.io" "Nkululeko docs" _blank
    click SA href "https://bagustris.github.io/speechain" "Speechain" _blank
    click PR href "https://bagustris.github.io/paperrag" "PaperRAG" _blank
    click GH href "https://github.com/bagustris" "GitHub profile" _blank
    click Tutorials href "/tutorials/" "Tutorials index"
    click SL href "https://bagustris.github.io/tutorial-shell" "Tutorial Shell" _blank
    click PY href "https://bagustris.github.io/python-for-signal-processing" "Python for Signal Processing" _blank
    click SP href "https://bagustris.github.io/speech-recognition-course" "Speech Recognition" _blank
    click GT href "https://bagustris.github.io/tutorial-git" "Tutorial Git" _blank
    click Pubs href "/publications/" "All publications"
    click AllP href "/publications/" "All publications"
    click Em href "mailto:bagustris@outlook.com" "Email"
    click GHub href "https://github.com/bagustris" "GitHub profile" _blank
    click Sch href "https://scholar.google.com/citations?user=xuiLAewAAAAJ&hl=en" "Google Scholar" _blank
    click CvPage href "/cv/" "Curriculum Vitae"
    click JA href "https://bagustris.github.io/bbj/" "Japanese learning" _blank
    click Blg href "https://bagustris.blogspot.com" "Blog" _blank
    click Th href "https://dspace.jaist.ac.jp/dspace/bitstream/10119/17472/2/paper.pdf" "PhD thesis" _blank
</pre>
