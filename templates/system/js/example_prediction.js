document.addEventListener("DOMContentLoaded", ()=>{
	DAN.$('pdf_button').onclick = () => {
        var element = document.getElementById('pdf_out');

        // Generate the PDF.
        html2pdf().from(element).set({
          margin: 1,
          filename: 'predict.pdf',
          html2canvas: { scale: 2 },
          jsPDF: {orientation: 'portrait', unit: 'in', format: 'letter', compressPDF: true}
        }).save();
    }
});