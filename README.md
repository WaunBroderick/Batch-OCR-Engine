
<HTML>
  <head>
  <meta charset="UTF-8">
  <meta name="description" content="Source code for the Batch-OCR-Engine project">
  <meta name="keywords" content="Python, OCR, NLP, NLTK, Computer, Vision, Document, AI, Tesseract, OpenCV">
  <meta name="author" content="Waun Broderick">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
  <h1>Batch-OCR-Engine</h1>
  
[![Build Status](https://travis-ci.com/WaunBroderick/INPROD.svg?branch=master)](https://travis-ci.com/WaunBroderick/INPROD)
![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django.svg)


  <center>
    <h2>Created by Waun Broderick </h2>
    <h4>Written in Python3.6.6</h4>
    <p>
      Batch-OCR-Engine tool uses OCR (Optical Character Recognition) to first read in all the words from a document and then uses NLP (Natural Language Processing) to pick necessary information for future actions. Currently it's in the process of automating Request For Information processes where TD Bank sends detailed information to Government agencies. This is the first use case for Batch-OCR-Engine but it can be potentially used anywhere and everywhere a documents needs to be read as part of a business process.

 

Some future applications of Batch-OCR-Engine are in reading return mail addresses, automatically creating summaries from credit applications, checking accuracy and details from uploaded documents and much much more. The tool has simple intuitive User interface for users with range of digital literacy.</center>
  
  
  <center><p>
  The first step of the tool is to read in clean high quality text data from any document using OCR. This utilizes Python libraries like OpenCV and Tesserect. The tool corrects for skew, brightness, sharpness, contrasts and color levels. The tool rechecks and modifies images not meeting internal quality control requirements utilizing Hyper Parameter tuning. The tool can understand 22 languages from English to Finnish. The tool automatically gets trained on new fonts by testing a limited amount of data. Finally Natural Language Tool Kit and Regular Expression are leveraged to pull information in structures reusable format. This information can then be utilized for the next step of process.

 

Batch-OCR-Engine has met the short term objective of demonstrating value of an AI based document reader but it will inculcate future advanced and differing requirements of different processes to become even more effective in future.

 
  </p></center>
  
  <h2>Dependencies</h2>
  <h4>Graphical Componenets</h4>
  <ul>
  <li>
    Tkinter
  </li>
  </ul>
  <h4>Conversions & Computer Vision</h4>
  <ul>
  <li>
    Tesseract 4.0
  </li>
  <li>
    Pillow 1.1.7
  </li>
    <li>
      wand 0.4.4
  </li>
    <li>
      PyPDF2 1.26.0
  </li>
    <li>
      scipy 1.1.0
  </li>
    <li>
      numpy 1.13.3
  </li>
  <li>
      GhostScript 9.23 (32bit)
  </li>
  <li>
    OpenCV 3.4.1
  </li>
  </ul>
   <h4>Deriving Understanding</h4>
  <ul>
  <li>
    nltk 3.3
  </li>
  <li>
    csv 1.0
  </li>
    <li>
      re 2.2.1
  </li>
  </ul>
   <h4>Algorithm Building</h4>
  <ul>
  <li>
    Threading
  </li>
    <li>
      pooling
  </li>
    <li>
      queueing
  </li>
  </ul>
   <h4>System Utilities</h4>
  <ul>
  <li>
    time
  </li>
    <li>
      os
  </li>
    <li>
      io
  </li>
    <li>
      shutil
  </li>
    <li>
      sys
  </li>
    <li>
      math
  </li>
  </ul>
  <h2>Interaction Diagram</h2>
  
  <h2>UML Diagram</h2>
  
</HTML>
