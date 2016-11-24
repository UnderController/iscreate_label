#include <vector>
#include "stdio.h"
#include <opencv2/opencv.hpp>
using namespace cv;
using namespace std;
Vec3b convolutionCalcullatePix(Mat &img_mat,Point position,Vec3b pos_default_val)
{
    int add_con_w =4;
    int sub_con_w =4;
    int add_con_h =4;
    int sub_con_h =4;
    int count = 0;
    int max_count = 0;
    Vec3b pos_val = pos_default_val;
    //判断卷积核的大小是否越界
    if(position.x < 4 ){
        sub_con_w = position.x;
    }else if(position.x+4 >= img_mat.cols){
        add_con_w = img_mat.cols-1 - position.x;
    }
    else{
        sub_con_w = 4;
        add_con_w = 4;

    }

    if(position.y < 4 ){
        sub_con_h = position.y;
    }else if(position.y+4 >= img_mat.rows){
        add_con_h = img_mat.rows-1 - position.y;
    }
    else{
        sub_con_h = 4;
        add_con_h = 4;
    }
    //统计卷积核中最多的像素点的值
    for(int j= position.x - sub_con_w; j < position.x + add_con_w;j++){
        for(int k= position.y - sub_con_h;k < position.y + add_con_h;k++){
            for(int l= j;l < position.x + add_con_w;l++){
                for(int m= k;m < position.y + add_con_h;m++){
                    //if(img_mat.at<Vec3b>(k,j) != pos_default_val /*&& img_mat.at<Vec3b>(k,j) != Vec3b(0,0,0)*/)
                    //{
                        if(img_mat.at<Vec3b>(k,j) == img_mat.at<Vec3b>(m,l))
                        {
                            count++;
                        }
                    //}//else{
                      //  l = position.x + add_con_w;
                      //  m = position.y + add_con_h;
                   // }
                }
            }
            //cout<<"count = "<<count<<endl;
            //cout<<"max_count"<<max_count<<endl;
            if(max_count <= count)
            {
                max_count = count;
                pos_val = img_mat.at<Vec3b>(k,j);
              //  cout<<k<<","<<j;
              //  cout<<"img_mat.at<Vec3b>(k,j) = "<<img_mat.at<Vec3b>(k,j)<<endl;
            }
            count = 0;

        }
    }
    max_count = 0;
    return pos_val;
}
vector <Vec3b>colorList()
{
    Vec3b road_val = Vec3b(0,192,0);
    Vec3b lane_mark_val = Vec3b(192,0,128);
    Vec3b sign_val = Vec3b(128,128,192);
    Vec3b traffic_light_val = Vec3b(0,0,255);
    Vec3b building_val = Vec3b(0,0,128);
    Vec3b tree_val = Vec3b(0,128,128);
    Vec3b sky_val = Vec3b(128,128,128);
    Vec3b pedestrain_val = Vec3b(200,200,130);
    Vec3b car_val = Vec3b(128,0,64);
    Vec3b animal_val = Vec3b(64,152,243);
    Vec3b white_val = Vec3b(255,255,255);
    vector <Vec3b>type_list_index;
    type_list_index.push_back(road_val);
    type_list_index.push_back(lane_mark_val);
    type_list_index.push_back(sign_val);
    type_list_index.push_back(traffic_light_val);
    type_list_index.push_back(building_val);
    type_list_index.push_back(tree_val);
    type_list_index.push_back(sky_val);
    type_list_index.push_back(pedestrain_val);
    type_list_index.push_back(car_val);
    type_list_index.push_back(animal_val);
    type_list_index.push_back(white_val);
    return type_list_index;
}
void voidPix2BlackPix(Mat &img_mat,vector<Vec3b> type_list_index)
{
    int t=0;
    for(int i=0;i<img_mat.rows;i++)
    {
        for(int j=0;j<img_mat.cols;j++)
        {
            for(t=0;t<type_list_index.size();t++){
                if(img_mat.at<Vec3b>(i,j) == type_list_index[t]){
                    break;
                }
            }
            if(t == type_list_index.size())
            {
                img_mat.at<Vec3b>(i,j) = Vec3b(0,0,0);
            }
        }
    }
    imshow("img_mat ",img_mat);
    imwrite("img_mat.png",img_mat);
    waitKey(0);
}

vector<Point> findTargetPixIndex(Mat &img_mat,Vec3b pix_val)
{
    Point pos;
    vector<Point> pos_index;

    for(int i=0;i<img_mat.rows;i++)
    {
        for(int j=0;j<img_mat.cols;j++)
        {
            if(img_mat.at<Vec3b>(i,j) == pix_val){
                pos.x = j;
                pos.y = i;
                pos_index.push_back(pos);

            }
        }
    }
    return pos_index;
}
int main(int argv, char **argc)
{
    char path[128] = "/home/iscreate/code/pic_deal_pix/save 2.png";

    Mat img_mat = imread(path);
    cout<<"img_mat = "<<img_mat.type()<<endl;
    cout<<"img_mat = "<<img_mat.channels()<<endl;

    vector<Point> pos_index;
    vector<Point> pos_index2;
    Vec3b pos_val = Vec3b(255,255,255);
     Vec3b pos_val2 = Vec3b(0,0,0);
    vector<Vec3b> pos_val_index;
    vector<Vec3b> pos_val_index2;
    vector<Vec3b> type_list_index;
    //获取颜色列表
    type_list_index = colorList();
    cout<<"type_list_index = "<<type_list_index.size()<<endl;

    //将图中颜色不是颜色列表的点变成黑色
    voidPix2BlackPix(img_mat,type_list_index);

    //找到白色像素点的位置
    pos_index = findTargetPixIndex(img_mat,Vec3b(255,255,255));
    //将白色像素点的值变成卷积核中颜色最多的值
    for(int i=0;i<pos_index.size();i++)
    {
        pos_val = convolutionCalcullatePix(img_mat,pos_index[i],Vec3b(255,255,255));
        pos_val_index.push_back(pos_val);
    }
    for(int i=0;i<pos_index.size();i++){
        img_mat.at<Vec3b>(pos_index[i].y,pos_index[i].x) = pos_val_index[i];
    }




    cout<<endl;
     cout<<endl;
      cout<<endl;
       cout<<endl;
        cout<<endl;
         cout<<endl;
          cout<<endl;
          cout<<endl;


          imshow("img_mat1",img_mat);
          imwrite("img_mat_withe.png",img_mat);
          waitKey(0);
    //找到黑色像素点的位置
    pos_index2 = findTargetPixIndex(img_mat,Vec3b(0,0,0));
    cout<<"pos_index2.size() = "<<pos_index2.size()<<endl;

    imshow("img_mat2",img_mat);
    imwrite("img_mat_withe.png",img_mat);
    waitKey(0);
    //将黑色像素点的值变成卷积核中颜色最多的值
    for(int i=000;i<pos_index2.size();i++)
    {
        pos_val2 = convolutionCalcullatePix(img_mat,pos_index2[i],Vec3b(0,0,0));

        cout<<i<<" "<<"pos_val2 ="<<pos_val2<<endl;
        pos_val_index2.push_back(pos_val2);
    }
    cout<<"pos_val_index2.size()"<<pos_val_index2.size()<<endl;
    //cout<<"pos_val_index[1010] ="<<pos_val_index2[1010]<<endl;
    for(int i=0;i<pos_index2.size();i++){
        cout<<"i "<<i<<endl;
        cout<<"pos_val_index2[i]"<<pos_val_index2[i]<<endl;
        cout<<"img_mat.at<Vec3b>(pos_index2[i].y,pos_index2[i].x)"<<img_mat.at<Vec3b>(pos_index2[i].y,pos_index2[i].x)<<endl;
        img_mat.at<Vec3b>(pos_index2[i].y,pos_index2[i].x) = pos_val_index2[i];
//        namedWindow("img_mat",CV_WINDOW_NORMAL);
//        imshow("img_mat",img_mat);
//        waitKey(0);
    }

    imshow("img_mat",img_mat);
    imwrite("img_mat_black.png",img_mat);
    waitKey(0);

    return 0;
}


