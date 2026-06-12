---
layout: single
permalink: /ja/
title: "音声・マルチモーダルAIの研究者・教育者"
description: "NAISTの音声AI研究者・教育者。音声処理とマルチモーダル処理に関するオープンソースツール（Nkululeko、Speechain）、チュートリアル、デモを公開しています。"
lang: ja
lang_ref: about
author_profile: true
redirect_from:
  - /ja/about/
  - /ja/about.html
---
> 実践せよ。読むだけで終わらない。

BTA は NAIST の音声 AI 研究者・教育者です。音声分類から ASR、TTS までの音声処理、そしてマルチモーダル情報融合に関する研究、教育、学生指導を行っています。

<pre class="mermaid">
mindmap
  root((BTA))
    研究
      音声AI
      マルチモーダル融合
      マルチタスク学習
      音声・音響分類
    ツール
      Nkululeko
      Speechain
      PaperRAG
      GitHub
    チュートリアル
      ShellとLinux
      PythonとDSP
      音声とオーディオ
      GitとLaTeX
    論文
      ICASSP
      O-COCOSDA
      APSIPA
      すべての論文
    日本語
      Ayo Belajar Bahasa Jepang
      みんなの日本語
      仕事のための日本語
    イスラム
      預言者物語
      アルバイン・ナワウィ
</pre>

<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';

const LINKS = {
  '研究':                    '/ja/research/',
  'ツール':                  '/tools/',
  'チュートリアル':          '/tutorials/',
  '論文':                    '/publications/',
  'すべての論文':            '/publications/',
  'Nkululeko':               'https://nkululeko.readthedocs.io',
  'Speechain':               'https://bagustris.github.io/speechain',
  'PaperRAG':                'https://bagustris.github.io/paperrag',
  'GitHub':                  'https://github.com/bagustris',
  'ShellとLinux':            'https://bagustris.github.io/tutorial-shell',
  'PythonとDSP':             'https://bagustris.github.io/python-for-signal-processing',
  '音声とオーディオ':        'https://bagustris.github.io/speech-recognition-course',
  'GitとLaTeX':              'https://bagustris.github.io/tutorial-git',
  'Email':                   'mailto:bagustris@outlook.com',
  'GitHub Profile':          'https://github.com/bagustris',
  'Google Scholar':          'https://scholar.google.com/citations?user=xuiLAewAAAAJ&hl=en',
  'CV':                      '/cv/',
  'Ayo Belajar Bahasa Jepang': 'https://bagustris.github.io/bbj/',
  'みんなの日本語':          'https://bagustris.github.io/minna-no-nihongo/',
  '仕事のための日本語':      'https://bagustris.github.io/japanese-for-work/',
  '預言者物語':              'https://bagustris.github.io/kisah-nabi',
  'アルバイン・ナワウィ':    'https://bagustris.github.io/arbain-nawawi',
  'ブログ':                  'https://bagustris.blogspot.com',
  '学位論文':                'https://dspace.jaist.ac.jp/dspace/bitstream/10119/17472/2/paper.pdf',
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
