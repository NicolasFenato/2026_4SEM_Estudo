# -*- coding: utf-8 -*-
"""Uso: python build.py ml|redes|cg|comp|bd   -> gera o DOCX em guias/<PASTA>/"""
import os, sys, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from guide_builder import Guide
CFG = {"ml": ("ML", "Guia_Machine_Learning"), "redes": ("REDES", "Guia_Redes"),
       "cg": ("COMP_G", "Guia_Computacao_Grafica"), "comp": ("COMPUTABILIDADE", "Guia_Computabilidade"),
       "bd": ("BD", "Guia_Banco_de_Dados")}
k = sys.argv[1]
folder, fname = CFG[k]
c = importlib.import_module("content_" + k)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", folder)
os.makedirs(out, exist_ok=True)
g = Guide(k.upper(), c.TITLE, c.COLOR, c.PROF, c.EXAM, c.SOURCES, topics=c.TOPICS,
          note=getattr(c, "NOTE", "Contas dos exercícios conferidas em Python; trechos marcados “Além dos slides” são complementos."))
path = os.path.join(out, fname + ".docx")
g.build(c.C, path)
print(os.path.abspath(path))
