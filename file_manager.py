import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, simpledialog
import os, shutil, datetime, threading, queue, sys

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

C = {
    "bg":"#02040a","bg2":"#050810","panel":"#060a14",
    "card":"#080d18","card2":"#0a1020",
    "cyan":"#00d4ff","cyan_dim":"#0099bb","cyan_glow":"#052535",
    "magenta":"#c850ff","magenta_dim":"#8833aa",
    "green":"#00ff88","green_dim":"#00aa55",
    "orange":"#ff8c42","red":"#ff4466","yellow":"#ffcc00",
    "text":"#e8edf8","text2":"#9ba8c0","text3":"#4a5570",
    "border":"#0f1a30","border2":"#162038","border_glow":"#0a1e2c",
    "row_a":"#04070f","row_b":"#060a16",
    "row_hover":"#0d1a30","row_sel":"#071830","row_sel_bd":"#00d4ff",
}

ICONS = {
    ".py":"🐍",".js":"🟨",".ts":"🔷",".jsx":"⚛",".tsx":"⚛",
    ".html":"🌐",".css":"🎨",".scss":"🎨",".json":"📋",
    ".xml":"📄",".yaml":"📄",".md":"📝",".txt":"📝",
    ".pdf":"📕",".doc":"📘",".docx":"📘",
    ".xls":"📗",".xlsx":"📗",".ppt":"📙",".pptx":"📙",
    ".jpg":"🖼",".jpeg":"🖼",".png":"🖼",".gif":"🖼",
    ".svg":"🖼",".webp":"🖼",".bmp":"🖼",
    ".mp4":"🎬",".avi":"🎬",".mkv":"🎬",".mov":"🎬",
    ".mp3":"🎵",".wav":"🎵",".flac":"🎵",
    ".zip":"📦",".rar":"📦",".tar":"📦",".gz":"📦",".7z":"📦",
    ".exe":"⚙️",".sh":"⚙️",".bat":"⚙️",
    ".sql":"🗄",".db":"🗄",".sqlite":"🗄",
    ".c":"💻",".cpp":"💻",".java":"☕",".go":"🔵",
    ".rs":"🦀",".rb":"💎",".php":"🐘",".kt":"🔶",
}

TYPES = {
    ".py":"Python",".js":"JavaScript",".ts":"TypeScript",
    ".html":"HTML",".css":"CSS",".json":"JSON",".xml":"XML",
    ".md":"Markdown",".txt":"Matn",".pdf":"PDF",
    ".doc":"Word",".docx":"Word",".xls":"Excel",".xlsx":"Excel",
    ".ppt":"PowerPoint",".pptx":"PowerPoint",
    ".jpg":"JPEG rasm",".jpeg":"JPEG rasm",".png":"PNG rasm",
    ".gif":"GIF rasm",".svg":"SVG rasm",".mp4":"MP4 video",
    ".avi":"AVI video",".mkv":"MKV video",
    ".mp3":"MP3 audio",".wav":"WAV audio",".flac":"FLAC audio",
    ".zip":"ZIP arxiv",".rar":"RAR arxiv",".tar":"TAR arxiv",
    ".gz":"GZ arxiv",".7z":"7-Zip arxiv",
    ".exe":"Dastur",".sh":"Shell skript",".bat":"Batch skript",
    ".sql":"SQL",".db":"Baza",".sqlite":"SQLite",
    ".c":"C tili",".cpp":"C++",".java":"Java",
    ".go":"Go",".rs":"Rust",".rb":"Ruby",".php":"PHP",
}

TYPE_CLR = {
    ".py":"#00d4ff",".js":"#ffcc00",".ts":"#4488ff",
    ".html":"#ff8c42",".css":"#c850ff",".json":"#00ff88",
    ".md":"#9ba8c0",".txt":"#9ba8c0",
    ".pdf":"#ff4466",".doc":"#4488ff",".docx":"#4488ff",
    ".xls":"#00ff88",".xlsx":"#00ff88",
    ".jpg":"#c850ff",".jpeg":"#c850ff",".png":"#c850ff",
    ".mp4":"#ff8c42",".mp3":"#ffcc00",
    ".zip":"#ffcc00",".rar":"#ffcc00",
    ".exe":"#ff4466",".sh":"#00ff88",
}

IS_MAC = sys.platform == "darwin"

def ficon(n,d): return "📁" if d else ICONS.get(os.path.splitext(n)[1].lower(),"📄")
def ftype(n,d):
    if d: return "Papka"
    e=os.path.splitext(n)[1].lower()
    return TYPES.get(e, f"{e[1:].upper()} fayli" if e else "Fayl")
def fsize(s):
    for u in ("B","KB","MB","GB","TB"):
        if s<1024: return f"{int(s)} {u}" if u=="B" else f"{s:.1f} {u}"
        s/=1024
    return f"{s:.1f} PB"
def fclr(n,d):
    if d: return C["cyan"]
    return TYPE_CLR.get(os.path.splitext(n)[1].lower(), C["text2"])


def bind_scroll(widget, callback):
    """macOS va boshqa platformalar uchun scroll binding."""
    if IS_MAC:
        widget.bind("<MouseWheel>", callback)
    else:
        widget.bind("<Button-4>", callback)
        widget.bind("<Button-5>", callback)
        widget.bind("<MouseWheel>", callback)


def bind_rightclick(widget, callback):
    """macOS va boshqa platformalar uchun right-click binding."""
    widget.bind("<Button-3>", callback)
    if IS_MAC:
        widget.bind("<Button-2>", callback)
        widget.bind("<Control-Button-1>", callback)


class Breadcrumb(ctk.CTkFrame):
    def __init__(self,master,on_click,**kw):
        super().__init__(master,fg_color=C["card"],corner_radius=10,**kw)
        self._cb=on_click
    def set(self,path):
        for w in self.winfo_children(): w.destroy()
        parts,p=[],path
        while True:
            h,t=os.path.split(p)
            if t: parts.insert(0,(t,p))
            elif h: parts.insert(0,(h,h)); break
            else: break
            if h==p: break
            p=h
        if len(parts)>5: parts=[("…",parts[0][1])]+parts[-4:]
        for i,(label,fp) in enumerate(parts):
            if i:
                tk.Label(self,text=" › ",bg=C["card"],fg=C["text3"],
                         font=("Consolas",12)).pack(side="left")
            last=i==len(parts)-1
            ctk.CTkButton(
                self,text=label,fg_color="transparent",
                hover_color=C["row_hover"],
                text_color=C["cyan"] if last else C["text2"],
                font=ctk.CTkFont("Consolas",12,weight="bold" if last else "normal"),
                height=30,corner_radius=6,
                command=lambda x=fp:self._cb(x)
            ).pack(side="left",padx=1)


class SearchBar(ctk.CTkFrame):
    def __init__(self,master,on_search,on_clear,**kw):
        super().__init__(master,fg_color=C["card"],corner_radius=12,
                         border_width=1,border_color=C["border2"],**kw)
        self._on_search=on_search; self._on_clear=on_clear
        self.mode="local"
        self._build()

    def _build(self):
        self._icon=tk.Label(self,text="🔍",bg=C["card"],fg=C["cyan"],
                            font=("Segoe UI Emoji",13))
        self._icon.pack(side="left",padx=(12,0))
        self._var=tk.StringVar()
        self._entry=tk.Entry(self,textvariable=self._var,
                             bg=C["card"],fg=C["text"],
                             insertbackground=C["cyan"],
                             relief="flat",font=("Consolas",12),
                             highlightthickness=0,bd=0)
        self._entry.pack(side="left",fill="x",expand=True,pady=10,padx=6)
        self._var.trace_add("write",lambda *_:self._fire())
        self._entry.bind("<Return>",lambda e:self._fire())
        self._entry.bind("<Escape>",lambda e:self._clear())
        clr=tk.Label(self,text="✕",bg=C["card"],fg=C["text3"],
                     font=("Consolas",11),cursor="hand2")
        clr.pack(side="left",padx=4)
        clr.bind("<Button-1>",lambda e:self._clear())
        tk.Frame(self,bg=C["border2"],width=1).pack(side="left",fill="y",pady=8)

        tf=tk.Frame(self,bg=C["card"])
        tf.pack(side="left",padx=10)
        self._btn_l=ctk.CTkButton(
            tf,text="📂 Joriy",width=82,height=28,
            fg_color=C["cyan_dim"],hover_color=C["cyan"],
            text_color=C["bg"],font=ctk.CTkFont("Consolas",10,"bold"),
            corner_radius=6,command=lambda:self._set_mode("local"))
        self._btn_l.pack(side="left",padx=2)
        self._btn_g=ctk.CTkButton(
            tf,text="🌐 Global",width=82,height=28,
            fg_color=C["card2"],hover_color=C["magenta_dim"],
            text_color=C["text2"],font=ctk.CTkFont("Consolas",10,"bold"),
            corner_radius=6,command=lambda:self._set_mode("global"))
        self._btn_g.pack(side="left",padx=2)
        self._mlbl=tk.Label(self,text="● Joriy papkada",
                            bg=C["card"],fg=C["cyan"],font=("Consolas",9))
        self._mlbl.pack(side="left",padx=(6,12))

    def _set_mode(self,m):
        self.mode=m
        if m=="local":
            self._btn_l.configure(fg_color=C["cyan_dim"],text_color=C["bg"])
            self._btn_g.configure(fg_color=C["card2"],text_color=C["text2"])
            self._mlbl.configure(text="● Joriy papkada",fg=C["cyan"])
            self._icon.configure(fg=C["cyan"])
            self._entry.configure(fg=C["text"],insertbackground=C["cyan"])
        else:
            self._btn_g.configure(fg_color=C["magenta_dim"],text_color=C["text"])
            self._btn_l.configure(fg_color=C["card2"],text_color=C["text2"])
            self._mlbl.configure(text="◉ Butun tizimda",fg=C["magenta"])
            self._icon.configure(fg=C["magenta"])
            self._entry.configure(fg=C["magenta"],insertbackground=C["magenta"])
        self._fire()

    def _fire(self):
        q=self._var.get().strip()
        if q: self._on_search(q,self.mode)
        else: self._on_clear()

    def _clear(self):
        self._var.set(""); self._on_clear()


class FileRow(tk.Frame):
    def __init__(self,master,item,idx,on_sel,on_open,on_right,**kw):
        bg=C["row_a"] if idx%2==0 else C["row_b"]
        super().__init__(master,bg=bg,height=38,cursor="hand2",**kw)
        self.pack_propagate(False)
        self._bg=bg; self._sel=False; self.item=item
        is_hidden = item["name"].startswith(".")
        dim = is_hidden
        self._bar=tk.Frame(self,bg=bg,width=3)
        self._bar.pack(side="left",fill="y")
        clr=fclr(item["name"],item["is_dir"])
        if dim: clr=C["text3"]
        self._ic=tk.Label(self,text=ficon(item["name"],item["is_dir"]),
                          bg=bg,fg=clr,font=("Segoe UI Emoji",12),width=3)
        self._ic.pack(side="left",padx=(4,2))
        name_fg = C["text3"] if dim else (clr if item["is_dir"] else C["text"])
        name_font = ("Consolas",10) if not dim else ("Consolas",10,"italic")
        self._nm=tk.Label(self,text=("· " if dim else "")+item["name"],bg=bg,
                          fg=name_fg,
                          font=name_font,anchor="w",width=34)
        self._nm.pack(side="left",padx=(0,4))
        self._sz=tk.Label(self,text=item["size"],bg=bg,fg=C["text3"],
                          font=("Consolas",9),width=10,anchor="e")
        self._sz.pack(side="left",padx=4)
        self._ty=tk.Label(self,text=item["type"],bg=bg,fg=C["text3"],
                          font=("Consolas",9),width=16,anchor="w")
        self._ty.pack(side="left",padx=8)
        self._dt=tk.Label(self,text=item["modified"],bg=bg,fg=C["text3"],
                          font=("Consolas",9),anchor="w",width=18)
        self._dt.pack(side="left",padx=4)
        if item.get("show_path"):
            p=item["entry"].path
            sh="…"+p[-40:] if len(p)>43 else p
            tk.Label(self,text=sh,bg=bg,fg=C["text3"],
                     font=("Consolas",8),anchor="w").pack(
                side="left",padx=6,fill="x",expand=True)
        self._ws=[self,self._bar,self._ic,self._nm,self._sz,self._ty,self._dt]
        for w in self._ws:
            w.bind("<Button-1>",        lambda e, s=self, i=item: on_sel(s, i))
            w.bind("<Double-Button-1>", lambda e, i=item: on_open(i))
            w.bind("<Enter>",           lambda e: self._hov(True))
            w.bind("<Leave>",           lambda e: self._hov(False))
            bind_rightclick(w, lambda e, i=item: on_right(e, i))

    def _hov(self,on):
        if self._sel: return
        bg=C["row_hover"] if on else self._bg
        for w in self._ws: w.configure(bg=bg)
        self._bar.configure(bg=C["cyan_glow"] if on else bg)

    def _sbg(self,bg):
        for w in self._ws: w.configure(bg=bg)

    def select(self,yes):
        self._sel=yes
        if yes:
            self._sbg(C["row_sel"]); self._bar.configure(bg=C["row_sel_bd"])
            self._nm.configure(fg=C["cyan"])
        else:
            self._sbg(self._bg); self._bar.configure(bg=self._bg)
            self._nm.configure(fg=C["cyan"] if self.item["is_dir"] else C["text"])


class FileManager(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Fayl Boshqaruvchi")
        self.geometry("1420x860"); self.minsize(960,640)
        self.configure(fg_color=C["bg"])
        self._cur=os.path.expanduser("~")
        self._hist=[self._cur]; self._hi=0
        self._items=[]; self._selrow=None; self._clip=None
        self._scol="name"; self._srev=False
        self._q=queue.Queue(); self._srch=False; self._gres=[]; self._spn=0
        self._show_hidden=False
        self._ui()
        self._load(self._cur,push=False)
        self._tick()

    def _ui(self):
        tb=tk.Frame(self,bg=C["panel"],height=64)
        tb.pack(fill="x"); tb.pack_propagate(False); self._topbar(tb)
        tk.Frame(self,bg=C["border_glow"],height=1).pack(fill="x")
        body=tk.Frame(self,bg=C["bg"])
        body.pack(fill="both",expand=True)
        sb=tk.Frame(body,bg=C["bg2"],width=260)
        sb.pack(side="left",fill="y"); sb.pack_propagate(False); self._sidebar(sb)
        tk.Frame(body,bg=C["border"],width=1).pack(side="left",fill="y")
        rp=tk.Frame(body,bg=C["bg"])
        rp.pack(side="left",fill="both",expand=True); self._rightpanel(rp)
        sf=tk.Frame(self,bg=C["panel"],height=28)
        sf.pack(fill="x"); sf.pack_propagate(False)
        tk.Frame(sf,bg=C["cyan"],width=3).pack(side="left",fill="y")
        self._stlbl=tk.Label(sf,text="  Tayyor",bg=C["panel"],fg=C["text3"],
                             font=("Consolas",9),anchor="w")
        self._stlbl.pack(side="left",fill="x",expand=True)
        self._cntlbl=tk.Label(sf,text="",bg=C["panel"],fg=C["cyan"],
                              font=("Consolas",9))
        self._cntlbl.pack(side="right",padx=14)

    def _topbar(self,p):
        lf=tk.Frame(p,bg=C["panel"])
        lf.pack(side="left",padx=(18,14),pady=10)
        tk.Label(lf,text="Abdulaziz",bg=C["panel"],fg=C["cyan"],
                 font=("Consolas",22,"bold")).pack()
        tk.Label(lf,text="FILE  MANAGER",bg=C["panel"],fg=C["text3"],
                 font=("Consolas",6)).pack()
        tk.Frame(p,bg=C["border2"],width=1).pack(side="left",fill="y",pady=10)
        nf=tk.Frame(p,bg=C["panel"])
        nf.pack(side="left",padx=10)
        for ico,cmd,col in[
            ("◀",self._back,C["cyan"]),("▶",self._fwd,C["cyan"]),
            ("▲",self._up,C["cyan"]),("↺",self._refresh,C["green"]),
        ]:
            ctk.CTkButton(nf,text=ico,width=40,height=40,
                          fg_color=C["card"],hover_color=C["row_hover"],
                          text_color=col,font=ctk.CTkFont("Consolas",17,"bold"),
                          corner_radius=8,border_width=1,border_color=C["border2"],
                          command=cmd).pack(side="left",padx=3)
        self.bc=Breadcrumb(p,on_click=self._load,height=48)
        self.bc.pack(side="left",fill="x",expand=True,padx=10)
        ctk.CTkButton(p,text="＋  Papka",width=110,height=40,
                      fg_color=C["card"],hover_color=C["green_dim"],
                      text_color=C["green"],border_width=1,border_color=C["green_dim"],
                      font=ctk.CTkFont("Consolas",11,"bold"),corner_radius=8,
                      command=self._newfolder).pack(side="right",padx=6)
        self._hid_btn=ctk.CTkButton(
            p,text="👁  Yashirin",width=120,height=40,
            fg_color=C["card"],hover_color=C["row_hover"],
            text_color=C["text3"],border_width=1,border_color=C["border2"],
            font=ctk.CTkFont("Consolas",10),corner_radius=8,
            command=self._toggle_hidden)
        self._hid_btn.pack(side="right",padx=6)

    def _sidebar(self,p):
        tk.Frame(p,bg=C["cyan"],width=2).place(x=0,y=0,relheight=1)
        def shdr(txt):
            f=tk.Frame(p,bg=C["bg2"])
            f.pack(fill="x",padx=(16,8),pady=(14,3))
            tk.Label(f,text=txt,bg=C["bg2"],fg=C["text3"],
                     font=("Consolas",8,"bold")).pack(side="left")
        shdr("⚡  TEZKOR O'TISH")
        sc=[
            ("🏠  Uy", os.path.expanduser("~")),
            ("🖥  Ish stoli", os.path.join(os.path.expanduser("~"),"Desktop")),
            ("⬇  Yuklangan", os.path.join(os.path.expanduser("~"),"Downloads")),
            ("📄  Hujjatlar",os.path.join(os.path.expanduser("~"),"Documents")),
            ("🖼  Rasmlar",  os.path.join(os.path.expanduser("~"),"Pictures")),
            ("🎵  Musiqa",   os.path.join(os.path.expanduser("~"),"Music")),
            ("🎬  Videolar", os.path.join(os.path.expanduser("~"),"Videos")),
            ("🗂  /  Ildiz", "/"),
        ]
        for lbl,path in sc:
            if os.path.exists(path):
                ctk.CTkButton(p,text=lbl,anchor="w",
                              fg_color="transparent",hover_color=C["row_hover"],
                              text_color=C["text2"],font=ctk.CTkFont("Consolas",11),
                              height=32,corner_radius=6,
                              command=lambda x=path:self._load(x)
                              ).pack(fill="x",padx=(16,8),pady=1)
        tk.Frame(p,bg=C["border2"],height=1).pack(fill="x",padx=12,pady=10)
        shdr("🌲  PAPKA DARAXTI")
        tw=tk.Frame(p,bg=C["bg2"])
        tw.pack(fill="both",expand=True,padx=(16,4))
        self._tcv=tk.Canvas(tw,bg=C["bg2"],highlightthickness=0,bd=0)
        tvsb=ctk.CTkScrollbar(tw,command=self._tcv.yview,fg_color=C["bg2"],
                              button_color=C["border2"],button_hover_color=C["border"])
        self._tcv.configure(yscrollcommand=tvsb.set)
        tvsb.pack(side="right",fill="y"); self._tcv.pack(fill="both",expand=True)
        self._tin=tk.Frame(self._tcv,bg=C["bg2"])
        self._twin=self._tcv.create_window((0,0),window=self._tin,anchor="nw")
        self._tin.bind("<Configure>",lambda e:self._tcv.configure(
            scrollregion=self._tcv.bbox("all")))
        self._tcv.bind("<Configure>",lambda e:self._tcv.itemconfig(
            self._twin,width=e.width))
        bind_scroll(self._tcv, self._scroll_tree)
        self._build_tree()
        tk.Frame(p,bg=C["border"],height=1).pack(fill="x",padx=8)
        inf=tk.Frame(p,bg=C["card"],height=46)
        inf.pack(fill="x",padx=8,pady=6); inf.pack_propagate(False)
        try:
            s=os.statvfs(os.path.expanduser("~"))
            txt=f"💾  {fsize(s.f_bavail*s.f_bsize)} bosh  /  {fsize(s.f_blocks*s.f_bsize)}"
        except: txt="💾  Disk malumoti mavjud emas"
        tk.Label(inf,text=txt,bg=C["card"],fg=C["text3"],
                 font=("Consolas",8)).pack(expand=True)

    def _build_tree(self):
        for w in self._tin.winfo_children(): w.destroy()
        self._tree_node(os.path.expanduser("~"),0,2)

    def _tree_node(self,path,ind,maxd):
        n=os.path.basename(path) or path
        pfx="▾ 📁 " if ind==0 else "  "*ind+"▸ 📁 "
        isc=path==self._cur
        ctk.CTkButton(self._tin,text=pfx+n,anchor="w",
                      fg_color=C["row_sel"] if isc else "transparent",
                      hover_color=C["row_hover"],
                      text_color=C["cyan"] if isc else C["text2"],
                      font=ctk.CTkFont("Consolas",10),height=26,corner_radius=4,
                      command=lambda p=path:self._load(p)).pack(fill="x",pady=0)
        if ind<maxd:
            try:
                ds=sorted([e for e in os.scandir(path)
                           if e.is_dir() and not e.name.startswith(".")],
                          key=lambda e:e.name.lower())[:10]
                for d in ds: self._tree_node(d.path,ind+1,maxd)
            except PermissionError: pass

    def _rightpanel(self,p):
        sq=tk.Frame(p,bg=C["bg"])
        sq.pack(fill="x",padx=12,pady=(10,0))
        self.sb=SearchBar(sq,on_search=self._onsearch,on_clear=self._onclear)
        self.sb.pack(fill="x")
        self._pf=tk.Frame(p,bg=C["bg"],height=24)
        self._pf.pack(fill="x",padx=14); self._pf.pack_propagate(False)
        self._plbl=tk.Label(self._pf,text="",bg=C["bg"],fg=C["magenta"],
                            font=("Consolas",9))
        self._plbl.pack(side="left",padx=4)
        self._stopbtn=ctk.CTkButton(self._pf,text="■ Toxtat",width=84,height=20,
                                    fg_color=C["card"],hover_color=C["red"],
                                    text_color=C["red"],
                                    font=ctk.CTkFont("Consolas",9),corner_radius=5,
                                    command=self._stopsearch)
        ch=tk.Frame(p,bg=C["card2"],height=34)
        ch.pack(fill="x",padx=12,pady=(6,0)); ch.pack_propagate(False)
        tk.Frame(ch,bg=C["border"],width=3).pack(side="left",fill="y")
        cols=[
            ("  Ad / Nom",None,36,"w"),("Hajm","size",10,"e"),
            ("Fayl turi","type",15,"w"),("Ozgartirilgan","modified",18,"w"),
        ]
        for lbl,cid,w,anc in cols:
            clr=C["cyan"] if (cid and cid==self._scol) else C["text3"]
            txt=lbl+("  "+("▼" if self._srev else "▲") if cid and cid==self._scol else "")
            f=tk.Frame(ch,bg=C["card2"],cursor="hand2" if cid else "arrow")
            f.pack(side="left",fill="y")
            lb=tk.Label(f,text=txt,bg=C["card2"],fg=clr,
                        font=("Consolas",9,"bold"),anchor=anc,width=w)
            lb.pack(fill="both",expand=True,padx=6)
            if cid:
                for ww in[f,lb]:
                    ww.bind("<Button-1>",lambda e,c=cid:self._sortby(c))
            if lbl!="Ozgartirilgan":
                tk.Frame(ch,bg=C["border"],width=1).pack(side="left",fill="y",pady=6)
        tk.Frame(p,bg=C["border_glow"],height=1).pack(fill="x",padx=12)
        lw=tk.Frame(p,bg=C["bg"])
        lw.pack(fill="both",expand=True,padx=12,pady=(0,4))
        self._cv=tk.Canvas(lw,bg=C["bg"],highlightthickness=0,bd=0)
        vsb=ctk.CTkScrollbar(lw,command=self._cv.yview,fg_color=C["bg"],
                             button_color=C["border2"],button_hover_color=C["border"])
        self._cv.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right",fill="y"); self._cv.pack(fill="both",expand=True)
        self._ff=tk.Frame(self._cv,bg=C["bg"])
        self._cw=self._cv.create_window((0,0),window=self._ff,anchor="nw")
        self._ff.bind("<Configure>",lambda e:self._cv.configure(
            scrollregion=self._cv.bbox("all")))
        self._cv.bind("<Configure>",lambda e:self._cv.itemconfig(self._cw,width=e.width))
        bind_scroll(self._cv, self._scroll)
        bind_scroll(self._ff, self._scroll)

    def _load(self,path,push=True):
        if not os.path.isdir(path): return
        if push:
            self._hist=self._hist[:self._hi+1]
            self._hist.append(path); self._hi+=1
        self._cur=path; self.bc.set(path)
        self._stopsearch(); self.sb._clear()
        self._render(path); self._setstatus(f"📂  {path}")
        self.after(80,self._build_tree)

    def _toggle_hidden(self):
        self._show_hidden = not self._show_hidden
        if self._show_hidden:
            self._hid_btn.configure(
                fg_color=C["cyan_dim"], hover_color=C["cyan"],
                text_color=C["bg"], border_color=C["cyan"],
                text="👁  Yashirin: ON")
        else:
            self._hid_btn.configure(
                fg_color=C["card"], hover_color=C["row_hover"],
                text_color=C["text3"], border_color=C["border2"],
                text="👁  Yashirin")
        self._refresh()

    def _back(self):
        if self._hi>0: self._hi-=1; self._load(self._hist[self._hi],push=False)
    def _fwd(self):
        if self._hi<len(self._hist)-1:
            self._hi+=1; self._load(self._hist[self._hi],push=False)
    def _up(self):
        p=os.path.dirname(self._cur)
        if p!=self._cur: self._load(p)
    def _refresh(self): self._load(self._cur,push=False)

    def _render(self,path,show_path=False):
        for w in self._ff.winfo_children(): w.destroy()
        self._selrow=None; self._items=[]
        try: entries=list(os.scandir(path))
        except PermissionError: self._empty("⛔  Ruxsat yoq"); return
        if not self._show_hidden:
            entries=[e for e in entries if not e.name.startswith(".")]
        dirs=sorted([e for e in entries if e.is_dir()],key=self._sk)
        files=sorted([e for e in entries if not e.is_dir()],key=self._sk)
        if self._srev: dirs.reverse(); files.reverse()
        for e in dirs+files:
            try: st=e.stat()
            except: st=None
            d=e.is_dir()
            self._items.append({
                "entry":e,"name":e.name,"is_dir":d,
                "size":"—" if d else (fsize(st.st_size) if st else "?"),
                "type":ftype(e.name,d),
                "modified":(datetime.datetime.fromtimestamp(st.st_mtime)
                            .strftime("%Y-%m-%d  %H:%M") if st else "—"),
                "show_path":show_path,
            })
        self._draw(self._items)
        self._cntlbl.configure(text=f"{len(self._items)} ta element")

    def _draw(self,items):
        for w in self._ff.winfo_children(): w.destroy()
        self._selrow=None
        if not items: self._empty("📭  Hech narsa topilmadi"); return
        for i,it in enumerate(items):
            row = FileRow(self._ff,it,i,
                    on_sel=self._selrow_fn,
                    on_open=self._open,
                    on_right=self._ctx)
            row.pack(fill="x")
            # Har bir row va uning bolalari uchun scroll binding (macOS)
            bind_scroll(row, self._scroll)
            for child in row.winfo_children():
                bind_scroll(child, self._scroll)

    def _empty(self,txt):
        f=tk.Frame(self._ff,bg=C["bg"])
        f.pack(fill="both",expand=True,pady=80)
        tk.Label(f,text=txt,bg=C["bg"],fg=C["text3"],
                 font=("Consolas",13)).pack()

    def _sk(self,e):
        try: st=e.stat()
        except: st=None
        if self._scol=="name": return e.name.lower()
        if self._scol=="size": return st.st_size if st else 0
        if self._scol=="type": return ftype(e.name,e.is_dir())
        if self._scol=="modified": return st.st_mtime if st else 0
        return e.name.lower()

    def _sortby(self,col):
        if self._scol==col: self._srev=not self._srev
        else: self._scol=col; self._srev=False
        self._refresh()

    def _onsearch(self,q,mode):
        self._stopsearch()
        if mode=="local": self._local(q)
        else: self._global(q)

    def _onclear(self):
        self._stopsearch()
        self._plbl.configure(text=""); self._stopbtn.pack_forget()
        self._render(self._cur)

    def _local(self,q):
        ql=q.lower()
        found=[it for it in self._items if ql in it["name"].lower()]
        self._draw(found)
        self._cntlbl.configure(text=f"{len(found)} / {len(self._items)} ta")
        self._setstatus(f"🔍  '{q}'  ·  Joriy papkada")

    def _global(self,q):
        self._srch=True; self._gres=[]
        self._draw([])
        self._plbl.configure(text=f"◉ Global: '{q}'…",fg=C["magenta"])
        self._stopbtn.pack(side="left",padx=4)
        root=os.path.expanduser("~")
        self._setstatus(f"🌐  Global qidiruv: '{q}'  ·  {root}")
        threading.Thread(target=self._worker,args=(q,root),daemon=True).start()

    def _worker(self,q,root):
        ql=q.lower()
        for dp,dns,fns in os.walk(root):
            if not self._srch: break
            dns[:]=[d for d in dns if not d.startswith(".")]
            names = dns + fns
            if not self._show_hidden:
                names = [n for n in names if not n.startswith(".")]
            for nm in names:
                if not self._srch: break
                if ql in nm.lower():
                    try:
                        es=list(os.scandir(dp))
                        m=next((x for x in es if x.name==nm),None)
                        if m:
                            try: st=m.stat()
                            except: st=None
                            d=m.is_dir()
                            self._q.put(("r",{
                                "entry":m,"name":m.name,"is_dir":d,
                                "size":"—" if d else (fsize(st.st_size) if st else "?"),
                                "type":ftype(m.name,d),
                                "modified":(datetime.datetime.fromtimestamp(st.st_mtime)
                                            .strftime("%Y-%m-%d  %H:%M") if st else "—"),
                                "show_path":True,
                            }))
                    except (PermissionError,OSError): pass
        self._q.put(("done",0))

    def _stopsearch(self):
        self._srch=False; self._gres=[]
        while not self._q.empty():
            try: self._q.get_nowait()
            except: pass

    def _tick(self):
        batch=[]
        try:
            while True:
                k,v=self._q.get_nowait()
                if k=="r": batch.append(v)
                elif k=="done":
                    self._srch=False
                    total=len(self._gres)
                    self._plbl.configure(text=f"✔  {total} ta topildi",fg=C["green"])
                    self._stopbtn.pack_forget()
                    self._cntlbl.configure(text=f"{total} ta natija")
        except queue.Empty: pass
        if batch:
            self._gres.extend(batch); self._draw(self._gres)
            self._cntlbl.configure(text=f"{len(self._gres)} ta…")
        if self._srch:
            self._spn=(self._spn+1)%4
            fr=["◐","◓","◑","◒"][self._spn]
            cur=self._plbl.cget("text")
            self._plbl.configure(text=fr+cur[1:])
        self.after(120,self._tick)

    def _selrow_fn(self,row,item):
        if self._selrow: self._selrow.select(False)
        self._selrow=row; row.select(True)

    def _open(self,item):
        if item["is_dir"]: self._load(item["entry"].path)
        else:
            import subprocess
            try:
                if sys.platform=="win32": os.startfile(item["entry"].path)
                elif sys.platform=="darwin": subprocess.Popen(["open",item["entry"].path])
                else: subprocess.Popen(["xdg-open",item["entry"].path])
            except Exception as ex: messagebox.showerror("Xato",str(ex))

    def _scroll(self, e):
        """macOS trackpad va boshqa platformalar uchun scroll."""
        if IS_MAC:
            # macOS delta — har bir event birlik, divide kerak emas
            self._cv.yview_scroll(int(-1 * e.delta), "units")
        else:
            if e.num == 4:
                self._cv.yview_scroll(-1, "units")
            elif e.num == 5:
                self._cv.yview_scroll(1, "units")
            else:
                self._cv.yview_scroll(int(-1 * (e.delta / 120)), "units")

    def _scroll_tree(self, e):
        """Sidebar tree uchun scroll."""
        if IS_MAC:
            self._tcv.yview_scroll(int(-1 * e.delta), "units")
        else:
            if e.num == 4:
                self._tcv.yview_scroll(-1, "units")
            elif e.num == 5:
                self._tcv.yview_scroll(1, "units")
            else:
                self._tcv.yview_scroll(int(-1 * (e.delta / 120)), "units")

    def _ctx(self, event, item):
        """Context menu — macOS va boshqa platformalar uchun."""
        m = tk.Menu(self, tearoff=0, bg=C["card"], fg=C["text"],
                    activebackground=C["row_sel"], activeforeground=C["cyan"],
                    font=("Consolas", 10), bd=0, relief="flat", activeborderwidth=0)
        m.add_command(label="  📋  Nusxa olish",     command=lambda: self._copy(item))
        m.add_command(label="  ✂️  Kochirish (Cut)",  command=lambda: self._cut(item))
        if self._clip:
            m.add_command(label="  📌  Joylashtirish", command=self._paste)
        m.add_separator()
        m.add_command(label="  ✏️  Nomini ozgartirish", command=lambda: self._rename(item))
        m.add_separator()
        m.add_command(label="  🗑️  Ochirish", foreground=C["red"],
                      command=lambda: self._delete(item))
        m.add_separator()
        m.add_command(label="  ℹ️  Xususiyatlar", command=lambda: self._props(item))
        try:
            m.tk_popup(event.x_root, event.y_root)
        except Exception:
            pass
        finally:
            try:
                m.grab_release()
            except Exception:
                pass

    def _copy(self,item):
        self._clip={"a":"copy","p":item["entry"].path}
        self._setstatus(f"📋  Nusxalandi: {item['name']}")

    def _cut(self,item):
        self._clip={"a":"cut","p":item["entry"].path}
        self._setstatus(f"✂️  Kesib olindi: {item['name']}")

    def _paste(self):
        if not self._clip: return
        src=self._clip["p"]; nm=os.path.basename(src)
        dst=os.path.join(self._cur,nm)
        if os.path.exists(dst):
            b,e=os.path.splitext(nm); dst=os.path.join(self._cur,f"{b}_nusxa{e}")
        try:
            if self._clip["a"]=="copy":
                (shutil.copytree if os.path.isdir(src) else shutil.copy2)(src,dst)
                self._setstatus(f"✅  Nusxalandi: {nm}")
            else:
                shutil.move(src,dst); self._clip=None
                self._setstatus(f"✅  Kochirish: {nm}")
            self._refresh()
        except Exception as ex: messagebox.showerror("Xato",str(ex))

    def _rename(self,item):
        nw=simpledialog.askstring("Nomini ozgartirish","Yangi nom:",
                                  initialvalue=item["name"],parent=self)
        if nw and nw!=item["name"]:
            try:
                os.rename(item["entry"].path,
                          os.path.join(os.path.dirname(item["entry"].path),nw))
                self._setstatus(f"✅  {nw}"); self._refresh()
            except Exception as ex: messagebox.showerror("Xato",str(ex))

    def _delete(self,item):
        if messagebox.askyesno("Ochirish",
            f"'{item['name']}' ni ochirmoqchimisiz?\nBu amal qaytarib bolmaydi!",
            icon="warning",parent=self):
            try:
                (shutil.rmtree if item["is_dir"] else os.remove)(item["entry"].path)
                self._setstatus(f"🗑️  Ochirildi: {item['name']}"); self._refresh()
            except Exception as ex: messagebox.showerror("Xato",str(ex))

    def _newfolder(self):
        nm=simpledialog.askstring("Yangi papka","Papka nomini kiriting:",parent=self)
        if nm:
            try:
                os.makedirs(os.path.join(self._cur,nm),exist_ok=True)
                self._setstatus(f"✅  Yaratildi: {nm}"); self._refresh()
            except Exception as ex: messagebox.showerror("Xato",str(ex))

    def _props(self,item):
        win=ctk.CTkToplevel(self)
        win.title("Xususiyatlar"); win.geometry("490x390")
        win.configure(fg_color=C["card"]); win.grab_set(); win.resizable(False,False)
        tk.Frame(win,bg=C["cyan"],height=3).pack(fill="x")
        hf=tk.Frame(win,bg=C["card"]); hf.pack(fill="x",padx=24,pady=(20,12))
        clr=fclr(item["name"],item["is_dir"])
        tk.Label(hf,text=ficon(item["name"],item["is_dir"]),
                 bg=C["card"],fg=clr,font=("Segoe UI Emoji",30)).pack(side="left")
        nf=tk.Frame(hf,bg=C["card"]); nf.pack(side="left",padx=14)
        tk.Label(nf,text=item["name"],bg=C["card"],fg=C["text"],
                 font=("Consolas",13,"bold"),wraplength=320,
                 anchor="w",justify="left").pack(anchor="w")
        tk.Label(nf,text=item["type"],bg=C["card"],fg=clr,
                 font=("Consolas",9)).pack(anchor="w")
        tk.Frame(win,bg=C["border_glow"],height=1).pack(fill="x",padx=24)
        try: st=item["entry"].stat()
        except: st=None
        rows=[
            ("📍 Joylashuv",os.path.dirname(item["entry"].path)),
            ("📦 Hajm",item["size"]),
            ("🕐 Ozgartirilgan",item["modified"]),
            ("📅 Yaratilgan",
             datetime.datetime.fromtimestamp(st.st_ctime).strftime(
                 "%Y-%m-%d  %H:%M") if st else "—"),
            ("🔑 Huquqlar",oct(st.st_mode)[-3:] if st else "—"),
        ]
        for k,v in rows:
            r=tk.Frame(win,bg=C["card2"],height=36)
            r.pack(fill="x",padx=16,pady=2); r.pack_propagate(False)
            tk.Label(r,text=k,bg=C["card2"],fg=C["text3"],
                     font=("Consolas",9),width=18,anchor="w").pack(side="left",padx=12)
            tk.Label(r,text=v,bg=C["card2"],fg=C["text"],font=("Consolas",9),
                     anchor="w",wraplength=280,justify="left").pack(
                side="left",fill="x",expand=True)
        ctk.CTkButton(win,text="✕  Yopish",fg_color=C["border2"],
                      hover_color=C["row_hover"],text_color=C["text2"],
                      font=ctk.CTkFont("Consolas",11),corner_radius=8,width=120,
                      command=win.destroy).pack(pady=16)

    def _setstatus(self,txt):
        self._stlbl.configure(text=f"  {txt}")


if __name__=="__main__":
    try: import customtkinter
    except ImportError:
        print("Onatilmagan:\n  pip install customtkinter"); raise SystemExit(1)
    FileManager().mainloop()