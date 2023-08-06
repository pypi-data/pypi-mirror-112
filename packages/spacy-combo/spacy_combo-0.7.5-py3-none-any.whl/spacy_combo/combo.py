#! /usr/bin/python3 -i
# coding=utf-8

import os,time,numpy,joblib.numpy_pickle
from spacy.symbols import LEMMA,POS,TAG,DEP,HEAD
from spacy.tokens import Doc
from spacy.language import Language
from spacy_combo.utils import Token,Tree

PACKAGE_DIR=os.path.abspath(os.path.dirname(__file__))
DOWNLOAD_DIR=os.path.join(PACKAGE_DIR,"models")
MODEL_URL="http://mozart.ipipan.waw.pl/~prybak/model_conll2018/"
UD_COLS=["id","form","lemma","upostag","xpostag","feats","head","deprel","deps","misc"]
SPACY_V3=hasattr(Language,"component")
tm=time.time()

class ComboParser(object):
  name="COMBO"
  def __init__(self,treebank,vocab):
    self.combo=load_combo(treebank)
    self.vocab=vocab
  def __call__(self,doc):
    trees=[]
    for id,s in enumerate(doc.sents):
      f={x:"__ROOT__" for x in UD_COLS}
      f["id"]=f["head"]="0"
      tokens=[Token(f)]
      for i,t in enumerate(s):
        f={x:"_" for x in UD_COLS}
        f["id"]=str(i+1)
        f["form"]=t.orth_
        f["xpostag"]=t.tag_ if t.tag_ else "_"
        f["misc"]="_" if t.whitespace_ else "SpaceAfter=No"
        tokens.append(Token(f))
      trees.append(Tree(id,tokens,[],[]))
    vs=self.vocab.strings
    r=vs.add("ROOT")
    words=[]
    lemmas=[]
    pos=[]
    tags=[]
    morphs=[]
    heads=[]
    deps=[]
    spaces=[]
    for s in self.combo.predict(trees):
      for t in s.tokens[1:]:
        f=t.fields
        words.append(f["form"])
        lemmas.append(vs.add(f["lemma"]))
        upos=f["upostag"]
        xpos=f["xpostag"]
        feats=f["feats"]
        pos.append(vs.add(upos))
        if xpos=="_" or xpos=="":
          xpos=upos if feats=="_" else upos+"_"+feats
        tags.append(vs.add(xpos))
        morphs.append(feats)
        deprel=f["deprel"]
        head=int(f["head"])
        if deprel=="root" or deprel=="ROOT" or head==0:
          heads.append(0)
          deps.append(r)
        else:
          heads.append(head-int(f["id"]))
          deps.append(vs.add(deprel))
        spaces.append(not "SpaceAfter=No" in f["misc"])
    doc=Doc(self.vocab,words=words,spaces=spaces)
    a=numpy.array(list(zip(lemmas,pos,tags,deps,heads)),dtype="uint64")
    doc.from_array([LEMMA,POS,TAG,DEP,HEAD],a)
    if SPACY_V3:
      for i,j in enumerate(morphs):
        if j!="_" and j!="":
          doc[i].set_morph(j)
    else:
      doc.is_tagged=True
      doc.is_parsed=True
    return doc

class ComboUnpickler(joblib.numpy_pickle.NumpyUnpickler):
  def find_class(self,module,name):
    if module in {"parser","encoders","models","mst","utils"}:
      module="spacy_combo."+module
    elif module.startswith("sklearn.externals.joblib"):
      module=module.replace("sklearn.externals.joblib","joblib")
    return super().find_class(module,name)

def progress(block_count,block_size,total_size):
  t=time.time()
  p=100.0*block_count*block_size/total_size
  if p<1:
    t=-1
  elif p>=100:
    p=100
    t-=tm
  else:
    t=(t-tm)*(100-p)/p
  b=int(p/2)
  if b==50:
    s="="*50
  else:
    s=("="*b)+">"+(" "*(49-b))
  if t<0:
    u="   "
  elif t<3600:
    u=time.strftime("%M:%S   ",time.gmtime(t))
  elif t<86400:
    u=time.strftime("%H:%M:%S   ",time.gmtime(t))
  else:
    u=time.strftime("%d+%H:%M:%S   ",time.gmtime(t))
  print("\r ["+s+"] "+str(int(p))+"% "+u,end="")

def download_combo(treebank):
  import urllib.request
  global tm
  os.makedirs(DOWNLOAD_DIR,exist_ok=True)
  tm=time.time()
  f,h=urllib.request.urlretrieve(MODEL_URL+"model."+treebank+".pkl",filename=os.path.join(DOWNLOAD_DIR,"model."+treebank+".pkl"),reporthook=progress)
  print("")

def load_combo(treebank):
  fn=os.path.join(DOWNLOAD_DIR,"model."+treebank+".pkl")
  if not os.path.isfile(fn):
    download_combo(treebank)
  with open(fn,"rb") as fh:
    u=ComboUnpickler(fn,fh)
    c=u.load()
  return c

def load_spacy(treebank):
  i=treebank.find("_")
  j=treebank if i<1 else treebank[0:i]
  try:
    exec("import spacy.lang."+j+" as p")
    exec("q=p."+locals()["p"].__all__[0])
    return locals()["q"]()
  except:
    from spacy.lang.xx import MultiLanguage
    return MultiLanguage()

def load(treebank):
  nlp=load_spacy(treebank)
  if SPACY_V3:
    nlp.add_pipe("sentencizer")
    Language.component("COMBO",func=ComboParser(treebank,nlp.vocab))
    nlp.add_pipe("COMBO")
  else:
    nlp.add_pipe(nlp.create_pipe("sentencizer"))
    nlp.add_pipe(ComboParser(treebank,nlp.vocab))
  nlp.meta["lang"]=treebank+"_COMBO"
  return nlp

