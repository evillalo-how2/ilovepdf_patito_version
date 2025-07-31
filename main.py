
import tkinter as tk
from tkinter import filedialog,messagebox,simpledialog
from tkinter import ttk
from PyPDF2 import PdfMerger,PdfReader,PdfWriter
from docx2pdf import convert
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class ilovePDFpatito:
    def __init__(self,root):
        self.root=root
        self.root.title("IlovePDFPatito")
        self.root.geometry("400x300")
        self.pdf_files=[]

        btn_frame=ttk.Frame(root)
        btn_frame.pack(pady=5)
        ttk.Button(root,text="+ Agregar PDF",command=self.select_pdfs).pack(pady=10)
        ttk.Button(root,text="⟶⟵ Unir PDF",command=self.merge_pdfs).pack(pady=10)
        ttk.Button(root,text="⟷ Dividir PDF",command=self.split_pdfs).pack(pady=10)
        #ttk.Button(root,text="Convertir PDF",command=self.convert_pdfs).pack(pady=10)
        
        btnm_move_delete=ttk.Frame(root)  
        btnm_move_delete.pack(pady=5)  
        tk.Button(root,text="↑ Subir PDF",command=self.pdf_upward).pack(pady=10)
        tk.Button(root,text="↓ Bajar PDF",command=self.pdf_downward).pack(pady=10)
        ttk.Button(root,text="Eliminar PDF seleccionado",command=self.delete_selected).pack(pady=10)
        ttk.Button(root,text="Eliminar lista de PDFs",command=self.clear_list).pack(pady=10)

        self.listbox=tk.Listbox(root,selectmode=tk.SINGLE,width=60,height=10)
        self.listbox.pack(pady=10,fill=tk.BOTH,expand=True)

        # ttk.Button(root,text=" comprimir PDF",command=self.compress_pdfs).pack(pady=10)

    def select_pdfs(self):
        files=filedialog.askopenfilenames(filetypes=[("PDF files","*.pdf")])
        for f in files:
            if f not in self.pdf_files:
                self.pdf_files.append(f)
                self.listbox.insert(tk.END, f.split("/")[-1])
        messagebox.showinfo("Archivos seleccionados", f"{len(files)} archivos seleccionados")


    def pdf_upward(self):
        place=self.listbox.curselection()
        if not place or place[0]==0:
            return
        place=place[0]
        self.pdf_files[place-1],self.pdf_files[place]=self.pdf_files[place],self.pdf_files[place-1]
        self.refresh_listbox()
        self.listbox.selection_set(place-1)

    def pdf_downward(self):
        place=self.listbox.curselection()
        if not place or place[0] == len(self.pdf_files)-1:
            return
        place=place[0]
        self.pdf_files[place+1],self.pdf_files[place]= self.pdf_files[place],self.pdf_files[place+1]
        self.refresh_listbox()
        self.listbox.selection_set(place+1)

    def delete_selected(self):
        place=self.listbox.curselection()
        if not place:
            return
        place=place[0]
        del self.pdf_files[place]
        self.refresh_listbox()

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for f in self.pdf_files:
            self.listbox.insert(tk.END, f.split("/")[-1])

    def clear_list(self):
        self.pdf_files=[]
        self.refresh_listbox()

    def merge_pdfs(self):
        if len(self.pdf_files) < 2:
            messagebox.showwarning("Advertencia","Para esta funcion necesitas minimo 2 archivos")
            return
        merger=PdfMerger()
    
        for pdf in self.pdf_files:
            merger.append(pdf)

        output_path=filedialog.asksaveasfilename(defaultextension=".pdf",filetypes=[("PDF","*.pdf")])
        if output_path:    
            merger.write(output_path)
            merger.close()
            messagebox.showinfo("Exito",f"PDFs unidos en {output_path}")


    def split_pdfs(self):
        idx = self.listbox.curselection()
        if not self.pdf_files or not idx:
            messagebox.showwarning("Advertencia", "Selecciona un PDF de la lista")
            return
        pdf_path = self.pdf_files[idx[0]]
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)
        rango = simpledialog.askstring("Dividir", f"Total de páginas: {total_pages}\n Ingresa rango (ej: 1-3)")
        if not rango:
            return
        try:
            inicio, fin = map(int, rango.split("-"))
            assert 1 <= inicio <= fin <= total_pages
        except:
            messagebox.showerror("Error", "Rango inválido. Debe ser por ejemplo: 1-3")
            return
        writer = PdfWriter()
        for i in range(inicio - 1, fin):
            writer.add_page(reader.pages[i])
        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if output_path:
            with open(output_path, "wb") as f:
                writer.write(f)
            messagebox.showinfo("Éxito", "Archivo dividido guardado")



if __name__ == "__main__":
    root = tk.Tk()
    app = ilovePDFpatito(root)
    root.mainloop()