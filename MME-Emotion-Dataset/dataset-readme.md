# 📚 MME-Emotion: A Holistic Evaluation Benchmark for Emotional Intelligence in Multimodal Large Language Models

**MME-Emotion** is a large-scale benchmark designed to evaluate the emotional intelligence of Multimodal Large Language Models (MLLMs). It contains **6,500 curated video clips** paired with **task-specific question-answering (QA) prompts**, covering **27 distinct real-world scenarios**. The benchmark formulates **eight representative emotional tasks**, including:

* Emotion Recognition in the Lab (ER-Lab)
* Emotion Recognition in the Wild (ER-Wild)
* Emotion Recognition under Noise (Noise-ER)
* Fine-Grained Emotion Recognition (FG-ER)
* Multi-Label Emotion Recognition (ML-ER)
* Sentiment Analysis (SA)
* Fine-Grained Sentiment Analysis (FG-SA)
* Intent Recognition (IR)

To enable a holistic and fair evaluation, MME-Emotion is equipped with a **multi-agent system framework** and a unified suite of **hybrid metrics** for both recognition accuracy and reasoning quality. This allows for comprehensive benchmarking of MLLMs across a wide spectrum of emotional understanding challenges.

---

## 🧪 Emotion Recognition in the Lab (ER-Lab)

Datasets collected in controlled laboratory environments with trained actors simulating real-life conversations. These samples feature rich facial expressions and clear speech, ensuring high-quality emotional data.

* **Dataset**: IEMOCAP  
  **Paper**: *IEMOCAP: Interactive emotional dyadic motion capture database*  
  **Link**: [https://sail.usc.edu/iemocap/](https://sail.usc.edu/iemocap/)  

---

## 🌍 Emotion Recognition in the Wild (ER-Wild)

Video clips extracted from movies, TV dramas, and short online videos. These datasets capture spontaneous and diverse emotional expressions in complex real-world scenarios, including variations in lighting, occlusion, and background noise.

* **Dataset**: CAER  
  **Paper**: *Context-Aware Emotion Recognition Networks*  
  **Link**: [https://caer-dataset.github.io/](https://caer-dataset.github.io/)  

* **Dataset**: MC-EIU  
  **Paper**: *Emotion and Intent Joint Understanding in Multimodal Conversation: A Benchmarking Dataset*  
  **Link**: [https://huggingface.co/datasets/YulangZhuo/MC-EIU](https://huggingface.co/datasets/YulangZhuo/MC-EIU)  

* **Dataset**: E3  
  **Paper**: *E³: Exploring Embodied Emotion Through A Large-Scale Egocentric Video Dataset*  
  **Link**: [https://github.com/Exploring-Embodied-Emotion-official/E3/blob/main/dataset/README.MD](https://github.com/Exploring-Embodied-Emotion-official/E3/blob/main/dataset/README.MD)  

* **Dataset**: MELD  
  **Paper**: *MELD: A Multimodal Multi-Party Dataset for Emotion Recognition in Conversation*  
  **Link**: [https://github.com/declare-lab/MELD](https://github.com/declare-lab/MELD)  

* **Dataset**: DFEW  
  **Paper**: *DFEW: A Large-Scale Database for Recognizing Dynamic Facial Expressions in the Wild*  
  **Link**: [https://dfew-dataset.github.io/download.html](https://dfew-dataset.github.io/download.html)  

* **Dataset**: MAFW  
  **Paper**: *MAFW: A Large-scale, Multi-modal, Compound Affective Database for Dynamic Facial Expression Recognition in the Wild*  
  **Link**: [https://mafw-database.github.io/MAFW/](https://mafw-database.github.io/MAFW/)  

---

## 🎧 Emotion Recognition under Noise (Noise-ER)

This task simulates real-world conditions by introducing artificial distortions such as resolution reduction and noise injection. It aims to evaluate the robustness of emotion recognition models under noisy and degraded conditions.

* **Dataset**: MER2024-Noise  
  **Paper**: *MER 2024: Semi-Supervised Learning, Noise Robustness, and Open-Vocabulary Multimodal Emotion Recognition*  
  **Link**: [https://huggingface.co/datasets/MERChallenge/MER2024](https://huggingface.co/datasets/MERChallenge/MER2024)  

---

## 🔬 Fine-Grained Emotion Recognition (FG-ER)

While traditional setting typically follows Ekman’s six basic emotions plus a neutral category, this task focuses on recognizing a broader and more nuanced set of emotions that better reflect the complexity of human affect through fine-grained body languages.

* **Dataset**: BOLD  
  **Paper**: *ARBEE: Towards automated recognition of bodily expression of emotion in the wild*  
  **Link**: [https://cydar.ist.psu.edu/emotionchallenge/dataset.php](https://cydar.ist.psu.edu/emotionchallenge/dataset.php)  

---

## 🏷️ Multi-Label Emotion Recognition (ML-ER)

In complex real-world scenarios, a single emotion label may be insufficient. This task allows multiple co-occurring emotional states to be identified, providing a more comprehensive understanding of user affect.

* **Dataset**: MAFW  
  **Paper**: *MAFW: A Large-scale, Multi-modal, Compound Affective Database for Dynamic Facial Expression Recognition in the Wild*  
  **Link**: [https://mafw-database.github.io/MAFW/](https://mafw-database.github.io/MAFW/)  

* **Dataset**: CMU-MOSEI  
  **Paper**: *Multimodal Language Analysis in the Wild: CMU-MOSEI Dataset and Interpretable Dynamic Fusion Graph*  
  **Link**: [http://multicomp.cs.cmu.edu/resources/cmu-mosei-dataset/](http://multicomp.cs.cmu.edu/resources/cmu-mosei-dataset/)  

---

## 😊 Sentiment Analysis (SA)

By combining visual, audio, and textual clues, multimodal sentiment analysis aims to detect users’ positive, negative, and neutral attitudes more accurately. This improves emotional state comprehension in natural interactions.

* **Dataset**: CMU-MOSEI  
  **Paper**: *Multimodal Language Analysis in the Wild*  
  **Link**: [http://multicomp.cs.cmu.edu/resources/cmu-mosei-dataset/](http://multicomp.cs.cmu.edu/resources/cmu-mosei-dataset/)  

* **Dataset**: CMU-MOSI  
  **Paper**: *MOSI: Multimodal Corpus of Sentiment Intensity and Subjectivity Analysis in Online Opinion Videos*  
  **Link**: [http://multicomp.cs.cmu.edu/resources/cmu-mosi-dataset/](http://multicomp.cs.cmu.edu/resources/cmu-mosi-dataset/)  

* **Dataset**: MELD  
  **Paper**: *MELD: A Multimodal Multi-Party Dataset for Emotion Recognition in Conversation*  
  **Link**: [https://github.com/declare-lab/MELD](https://github.com/declare-lab/MELD)  

* **Dataset**: CH-SIMS v2.0  
  **Paper**: *Make Acoustic and Visual Cues Matter: CH-SIMS v2.0 Dataset and AV-Mixup Consistent Module*  
  **Link**: [https://thuiar.github.io/sims.github.io/chsims](https://thuiar.github.io/sims.github.io/chsims)  

---

## 🎯 Fine-Grained Sentiment Analysis (FG-SA)

This task goes beyond basic sentiment categories to capture subtle emotional intensity levels such as “weak positive” or “very strong negative.” It enables systems to understand fine-grained shifts in user sentiment for deeper and more sensitive emotional reasoning.

* **Dataset**: CMU-MOSI  
  **Paper**: *MOSI: Multimodal Corpus of Sentiment Intensity and Subjectivity Analysis in Online Opinion Videos*  
  **Link**: [http://multicomp.cs.cmu.edu/resources/cmu-mosi-dataset/](http://multicomp.cs.cmu.edu/resources/cmu-mosi-dataset/)  

---

## 🗣️ Intent Recognition (IR)

Multimodal intent recognition aims to jointly infer users’ emotional states and underlying intentions. By leveraging audio, visual, and textual information, models can better understand users’ communicative goals and contextual needs.

* **Dataset**: MC-EIU  
  **Paper**: *Emotion and Intent Joint Understanding in Multimodal Conversation: A Benchmarking Dataset*  
  **Link**: [https://huggingface.co/datasets/YulangZhuo/MC-EIU](https://huggingface.co/datasets/YulangZhuo/MC-EIU)  

---

## 📖 Citation

If you use the **MME-Emotion benchmark** or find any of the following datasets helpful for your research, please consider citing the corresponding papers:

```bibtex
@article{busso2008iemocap,
  title={IEMOCAP: Interactive emotional dyadic motion capture database},
  author={Busso, Carlos and Bulut, Murtaza and Lee, Chi-Chun and Kazemzadeh, Abe and Mower, Emily and Kim, Samuel and Chang, Jeannette N and Lee, Sungbok and Narayanan, Shrikanth S},
  journal={Language Resources and Evaluation},
  volume={42},
  pages={335--359},
  year={2008},
  publisher={Springer}
}

@inproceedings{lee2019context,
  title={Context-Aware Emotion Recognition Networks},
  author={Lee, Jiyoung and Kim, Seungryong and Kim, Sunok and Park, Jungin and Sohn, Kwanghoon},
  booktitle={Proceedings of the IEEE/CVF International Conference on Computer Vision},
  pages={10143--10152},
  year={2019}
}

@article{liu2024emotion,
  title={Emotion and Intent Joint Understanding in Multimodal Conversation: A Benchmarking Dataset},
  author={Liu, Rui and Zuo, Haolin and Lian, Zheng and Xing, Xiaofen and Schuller, Bj{\"o}rn W and Li, Haizhou},
  journal={arXiv preprint arXiv:2407.02751},
  year={2024}
}

@article{feng20243,
  title={$E^3$: Exploring Embodied Emotion Through A Large-Scale Egocentric Video Dataset},
  author={Feng, Yueying and Han, WenKang and Jin, Tao and Zhao, Zhou and Wu, Fei and Yao, Chang and Chen, Jingyuan and others},
  journal={Advances in Neural Information Processing Systems},
  volume={37},
  pages={118182--118197},
  year={2024}
}

@article{poria2018meld,
  title={MELD: A Multimodal Multi-Party Dataset for Emotion Recognition in Conversations},
  author={Poria, Soujanya and Hazarika, Devamanyu and Majumder, Navonil and Naik, Gautam and Cambria, Erik and Mihalcea, Rada},
  journal={arXiv preprint arXiv:1810.02508},
  year={2018}
}

@inproceedings{jiang2020dfew,
  title={DFEW: A Large-Scale Database for Recognizing Dynamic Facial Expressions in the Wild},
  author={Jiang, Xingxun and Zong, Yuan and Zheng, Wenming and Tang, Chuangao and Xia, Wanchuang and Lu, Cheng and Liu, Jiateng},
  booktitle={Proceedings of the 28th ACM International Conference on Multimedia},
  pages={2881--2889},
  year={2020}
}

@inproceedings{liu2022mafw,
  title={MAFW: A Large-Scale, Multi-Modal, Compound Affective Database for Dynamic Facial Expression Recognition in the Wild},
  author={Liu, Yuanyuan and Dai, Wei and Feng, Chuanxu and Wang, Wenbin and Yin, Guanghao and Zeng, Jiabei and Shan, Shiguang},
  booktitle={Proceedings of the 30th ACM International Conference on Multimedia},
  pages={24--32},
  year={2022}
}

@inproceedings{lian2024mer,
  title={MER 2024: Semi-Supervised Learning, Noise Robustness, and Open-Vocabulary Multimodal Emotion Recognition},
  author={Lian, Zheng and Sun, Haiyang and Sun, Licai and Wen, Zhuofan and Zhang, Siyuan and Chen, Shun and Gu, Hao and Zhao, Jinming and Ma, Ziyang and Chen, Xie and others},
  booktitle={Proceedings of the 2nd International Workshop on Multimodal and Responsible Affective Computing},
  pages={41--48},
  year={2024}
}

@article{luo2020arbee,
  title={ARBEE: Towards Automated Recognition of Bodily Expression of Emotion in the Wild},
  author={Luo, Yu and Ye, Jianbo and Adams, Reginald B and Li, Jia and Newman, Michelle G and Wang, James Z},
  journal={International Journal of Computer Vision},
  volume={128},
  pages={1--25},
  year={2020},
  publisher={Springer}
}

@inproceedings{zadeh2018multimodal,
  title={Multimodal Language Analysis in the Wild: CMU-MOSEI Dataset and Interpretable Dynamic Fusion Graph},
  author={Zadeh, AmirAli Bagher and Liang, Paul Pu and Poria, Soujanya and Cambria, Erik and Morency, Louis-Philippe},
  booktitle={Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)},
  pages={2236--2246},
  year={2018}
}

@article{zadeh2016mosi,
  title={MOSI: Multimodal Corpus of Sentiment Intensity and Subjectivity Analysis in Online Opinion Videos},
  author={Zadeh, Amir and Zellers, Rowan and Pincus, Eli and Morency, Louis-Philippe},
  journal={arXiv preprint arXiv:1606.06259},
  year={2016}
}

@inproceedings{liu2022make,
  title={Make Acoustic and Visual Cues Matter: CH-SIMS v2.0 Dataset and AV-Mixup Consistent Module},
  author={Liu, Yihe and Yuan, Ziqi and Mao, Huisheng and Liang, Zhiyun and Yang, Wanqiuyue and Qiu, Yuanzhe and Cheng, Tie and Li, Xiaoteng and Xu, Hua and Gao, Kai},
  booktitle={Proceedings of the 2022 International Conference on Multimodal Interaction},
  pages={247--258},
  year={2022}
}
```

