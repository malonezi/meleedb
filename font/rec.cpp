#include <tesseract/baseapi.h>
#include <leptonica/allheaders.h>

int main()
{
    char *outText;
    
    char *configs[] = {"/usr/share/tessdata/configs/bazaar"};

    tesseract::TessBaseAPI *api = new tesseract::TessBaseAPI();
    // Initialize tesseract-ocr with English, without specifying tessdata path
    if (api->Init(NULL, "eng", tesseract::OEM_DEFAULT, configs, 1, NULL, NULL, false)) {
        fprintf(stderr, "Could not initialize tesseract.\n");
        exit(1);
    }

    api->SetVariable("user_words_suffix","states");
    api->SetVariable("enable_new_segsearch","1");
    api->SetVariable("language_model_penalty_non_dict_word","1");
    api->SetVariable("tessedit_char_whitelist","ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890");

    api->PrintVariables(stdout);

    // Open input image with leptonica library
    Pix *image = pixRead("frames/dump0100.png");
    api->SetImage(image);

    api->SetRectangle(380, 60, 300, 60);

    // Get OCR result
    outText = api->GetUTF8Text();
    printf("OCR output:\n%s", outText);

    // Destroy used object and release memory
    api->End();
    delete [] outText;
    pixDestroy(&image);

    return 0;
}
