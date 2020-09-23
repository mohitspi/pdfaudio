def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.document.name = form.cleaned_data.get('document')

            
            print(user.document.name)
            module_dir = os.path.dirname(__file__)
            translator = Translator()
            pdfFileObj = open(str(user.document.name), 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            print(pdfReader.numPages)
            pageObj = pdfReader.getPage(0)
            String_text = pageObj.extractText()
            name = str(user.document.name)[:-4]+".txt"
            with open(name, "w", encoding="utf-8") as f:
                f.write(String_text)
            pdfFileObj.close()
            data_file = open(name , 'r', encoding="utf-8")
            data = data_file.read().encode().decode('utf-8')
            translation = translator.translate(data, dest="hi", encoding="utf-8")
            print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")
            my = {translation.text}
            final_file = gTTS(text=str(my), lang="hi")
            outFileName = 'D:\\audio\\myapp\\static\\audio\\'+str(user.document.name)[:-4]+".mp3"
            final_file.save(outFileName)
            print('success')
    else:
        form = DocumentForm()
    document = Document.objects.all().last()
    return render(request, 'demo.html', {
        'form': form, 'outFileName': outFileName
    })