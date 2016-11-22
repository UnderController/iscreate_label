void WaterCanny(InputArray _water, InputArray _canny){
    Mat water = _water.getMat();
    Mat canny = _canny.getMat();

    w = water.cols;
    h = water.rows;


    for(int i = 0;i < h; i++){
        uchar water_data = water.ptr<uchar>;

        for(int j = 0; j < w; j++){
            water_data[j] =
        }
    }
}
