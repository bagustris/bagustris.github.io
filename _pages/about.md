---
permalink: /
title: "Speech and Multimodal AI Researcher"
description: "Speech AI researcher and educator building open-source tools, courses, tutorials, and demos in speech, acoustic and multimodal processing."
lang: en
lang_ref: about
author_profile: true
redirect_from:
  - /about/
  - /about.html
---
> Do! Don’t just read.

BTA is a speech AI researcher and educator at NAIST. He does research, teaching, and supervising in speech processing — from speech classification to ASR and TTS —, to acoustics and multimodal information fusion. Diagram below shows the connection between multimodal, acoustics, and speech, in which each concept is part of larger concept. Multimodal fusion combines information from multiple modalities, such as audio, visual, and text. Acoustics focuses on the physical properties of sound and how it is produced, transmitted, and perceived, including music, speech, and noise. Speech processing involves analyzing and understanding human speech signals for various applications.

<p align="center">
 <img src="../images/research_bta_en.png" alt="Research areas: speech, acoustics, multimodal">
</p>

Below is a mindmap of BTA's research, tools, tutorials, courses, publications, and other interests. Click on the nodes to explore more.  

<pre class="mermaid">
mindmap
  root((BTA))
    Tools
      Nkululeko
      Speechain
      PaperRAG
      Audiokit
      Sherox
    Publications
      Speech Communication
      ICASSP
      Interspeech
      O-COCOSDA
      APSIPA
    Tutorials
      Shell and Linux
      Python Tutorial
      Shell extras
    Courses
      Speech Recognition Course
      Python for Signal Processing
      Multimodal Processing
      Basic Mathematics
    Japanese
      Ayo Belajar Bahasa Jepang
      Minna no Nihongo
      Japanese for Work
      Kanji Drills
      Kotoba  
      JLPT  
      JED
      Wani Kanji
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
  'Speech AI':              'https://nkululeko.readthedocs.io/en/latest/',
  'Multimodal Fusion':      'https://human-ai-lab.github.io/multibench/',
  'Nkululeko':              'https://github.com/felixbur/nkululeko',
  'Speechain':              'https://bagustris.github.io/speechain',
  'PaperRAG':               'https://bagustris.github.io/paperrag',
  'Audiokit':               'https://github.com/bagustris/audiokit',
  'Sherox':                 'https://github.com/bagustris/sherox',
  'Shell and Linux':        'https://bagustris.github.io/tutorial-shell',
  'Python tutorial':        'https://bagustris.github.io/python-tutorial',
  'Shell extras':           'https://bagustris.github.io/shell-extras',
  'Speech Recognition Course': 'https://bagustris.github.io/speech-recognition-course',
  'Python for Signal Processing': 'https://bagustris.github.io/python-for-signal-processing',
  'Multimodal Processing':  'https://bagustris.github.io/multisensory',
  'Basic Mathematics':      'https://bagustris.github.io/matematika/',
  'Email':                  'mailto:bagustris@outlook.com',
  'GitHub Profile':         'https://github.com/bagustris',
  'Google Scholar':         'https://scholar.google.com/citations?user=xuiLAewAAAAJ&hl=en',
  'CV':                     '/cv/',
  'Ayo Belajar Bahasa Jepang':      'https://bagustris.github.io/bbj/',
  'Minna no Nihongo':       'https://bagustris.github.io/minna-no-nihongo/',
  'Japanese for Work':      'https://bagustris.github.io/japanese-for-work/',
  'Kanji Drills':           'https://bagustris.github.io/kanji-drill/',
  'Kotoba':                 'https://bagustris.github.io/kotoba/',
  'JLPT':                   'https://bagustris.github.io/jlpt/',
  'JED':                    'https://bagustris.github.io/jed/',
  'Wani Kanji':             'https://bagustris.github.io/wanikanji/', 
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
