# SciTweets-Emo
Emotion Analysis on informal online scientific discourse

This repository contains our work towards a new annotation of the SciTweets dataset along with the accompanying analysis. Both of the annotation layers were done manually, the first one labeled the tweets based on their science relatedness. The four label for that layer are scientific claim, scientific context, scientific reference, non science related. The second annotation layer was done according to the emotions the tweets convey, using Ekman's Model.
The work presented here was conducted between january and July 2025 by four computer science students : Tony BESSE, Lucien BOUBY, Alain LE et Anton Verbovyi.

## Table of Content

This repository contains five major parts :

1. **SciTweets-Emo** - The dataset obtained by the three annotators through their annotation process.
2. **Annotation** - Information about the annotation work including the annotation process, annotation guide, Fleiss' Kappa and final file creation process.  It also includes individual annotations from each annotator.
3. **Analysis** - Contains all the visualizations and data created for the analysis of the SciTweets-Emo dataset, as well as the code used to generate them.
4. **Classifier** - This directory includes our experiments and attempts at emotion classification.
5. **Rapport_TER_ICO_2025** summary of the work carried out by Tony BESSE, Alain LE et Anton Verbovyi, focusing on annotation, classification, and early-stage analysis.

## The SciTweets dataset

The SciTweets dataset has been published by Hafid, Salim in "SciTweets - A Dataset and Annotation Framework for Detecting Scientific Online Discourse", et al you can find it here https://github.com/AI-4-Sci/SciTweets?tab=readme-ov-file and read more about it here https://arxiv.org/abs/2206.07360.