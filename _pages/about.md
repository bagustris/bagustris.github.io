---
permalink: /
title: "Speech and Multimodal AI Researcher and Educator"
description: "Speech AI researcher and educator at NAIST building open-source tools (Nkululeko, Speechain), tutorials, and demos in speech processing and multimodal processing."
lang: en
lang_ref: about
author_profile: true
redirect_from:
  - /about/
  - /about.html
---
> Do! Don’t just read.

BTA is a speech AI researcher and educator at NAIST. I do research, teaching, 
tutorials, and demos in speech processing — from speech classification
(e.g., emotion recognition) to ASR and TTS — and multimodal information fusion.

<pre class="mermaid">
mindmap
  root((BTA))
    Research
      Speech AI
      Multimodal Fusion
      Multitask Learning
      Speech/Audio Classification  
    Tools
      Nkululeko
      Speechain
      PaperRAG
      GitHub
    Tutorials
      Shell and Linux
      Python and DSP
      Speech and Audio
      Git and LaTeX
    Publications
      ICASSP
      O-COCOSDA  
      APSIPA
      All Publications
    Japanese
      Ayo Belajar Bahasa Jepang
      Minna no Nihongo
      Japanese for Work
    Islam
      Kisah Nabi 
      Arbain Nawawi
</pre>

<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';

const LINKS = {
  'Research':               '/research/',
  'Tools':                  '/tools/',
  'Tutorials':              '/tutorials/',
  'Publications':           '/publications/',
  'All Publications':       '/publications/',
  'Nkululeko':              'https://nkululeko.readthedocs.io',
  'Speechain':              'https://bagustris.github.io/speechain',
  'PaperRAG':               'https://bagustris.github.io/paperrag',
  'GitHub':                 'https://github.com/bagustris',
  'Shell and Linux':        'https://bagustris.github.io/tutorial-shell',
  'Python and DSP':         'https://bagustris.github.io/python-for-signal-processing',
  'Speech and Audio':       'https://bagustris.github.io/speech-recognition-course',
  'Git and LaTeX':          'https://bagustris.github.io/tutorial-git',
  'Email':                  'mailto:bagustris@outlook.com',
  'GitHub Profile':         'https://github.com/bagustris',
  'Google Scholar':         'https://scholar.google.com/citations?user=xuiLAewAAAAJ&hl=en',
  'CV':                     '/cv/',
  'Ayo Belajar Bahasa Jepang':      'https://bagustris.github.io/bbj/',
  'Minna no Nihongo':       'https://bagustris.github.io/minna-no-nihongo/',
  'Japanese for Work':      'https://bagustris.github.io/japanese-for-work/',
  'Kisah Nabi':             'https://bagustris.github.io/kisah-nabi',
  'Arbain Nawawi':          'https://bagustris.github.io/arbain-nawawi',
  'Blogs':                  'https://bagustris.blogspot.com',
  'Theses':                 'https://dspace.jaist.ac.jp/dspace/bitstream/10119/17472/2/paper.pdf',
};

mermaid.initialize({ startOnLoad: false, securityLevel: 'loose' });

mermaid.run({ querySelector: '.mermaid' }).then(() => {
  document.querySelectorAll('.mermaid svg').forEach(svg => {
    svg.querySelectorAll('foreignObject p, text').forEach(el => {
      const label = el.textContent.trim();
      const href = LINKS[label];
      if (!href) return;
      const node = el.closest('g');
      if (!node) return;
      node.style.cursor = 'pointer';
      node.addEventListener('click', e => {
        e.stopPropagation();
        href.startsWith('/') || href.startsWith('mailto:')
          ? (window.location.href = href)
          : window.open(href, '_blank');
      });
    });
  });
});
</script>
