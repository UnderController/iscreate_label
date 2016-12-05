#include <vector>
#include "stdio.h"
#include <opencv2/opencv.hpp>
using namespace cv;
using namespace std;

//卷积核的大小为9x9，以一个点为中心上下左右减4变成9x9的卷积核
int con_kernel_size = 4;
int threshold_val = 30;


// 对图像中定位到的颜色的像素值统计它周围颜色最多点的像素值
// @img_mat 传入图像的mat矩阵
// @position 想要改变颜色点的坐标
// @ pos_deault_val 该点本来的像素值
// @threshold 卷积核中如果它自身颜色的像素值最多，并且大于阈值改点的颜色将不会被改变
Vec3b convolutioncalcullatepix(Mat &img_mat,Point position,Vec3b pos_default_val,int threshold)
{
    int count = 0;
    int max_count = 0;
    int sec_max_count =0;
    vector<Vec3b> con_kernel;
    Vec3b pos_val = pos_default_val;
    Vec3b sec_pos_val = pos_default_val;
    //统计卷积核中最多的像素点的值
    for(int j= position.x - con_kernel_size; j < position.x + con_kernel_size;j++){
        for(int k= position.y - con_kernel_size;k < position.y + con_kernel_size;k++){
            for(int l= j;l < position.x + con_kernel_size;l++){
                for(int m= k;m < position.y + con_kernel_size;m++){
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
            //统计颜色最多点的像素值
            if(max_count <= count)
            {
                if(sec_pos_val != pos_val)
                {
                    sec_max_count = count;
                    sec_pos_val = pos_val;
                }
                max_count = count;
                pos_val = img_mat.at<Vec3b>(k,j);
            }
            count = 0;

        }
    }
    //待处理颜色的点在一个卷积核中大于阈值时才返回该颜色的值不然返回卷积核中其它颜色较多点的值
    if(pos_val != pos_default_val)
    {
        return pos_val;
    }else if(pos_val == pos_default_val && max_count>threshold){
        return pos_val;
    }else{
        return sec_pos_val;
    }

}



vector <Vec3b>colorlist()
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
    // Vec3b white_val = Vec3b(255,255,255);
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
    //type_list_index.push_back(white_val);
    return type_list_index;
}
//将图中颜色不是颜色列表的点改变成其它的颜色
// @img_mat 传入图像的mat矩阵
// @type_list_index 要处理点的索引
// @turn_to_val 要处理的点要变成什么颜色
void otherpixval2intendpixval(Mat &img_mat,vector<Vec3b> type_list_index,Vec3b turn_to_val)
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
                img_mat.at<Vec3b>(i,j) = turn_to_val;
            }
        }
    }
}

// 除去图中离散的点并将它变成他周围颜色最多点的值
// @img_mat 传入图像的mat矩阵
// @pix_val 要改变颜色点的像素值
// @threshold 卷积核中如果它自身颜色的像素值最多，并且大于阈值改点的颜色将不会被改变
void removediscretedot(Mat &img_mat,Vec3b pix_val,int threshold,int pading)
{
    Point pos;
    vector<Point> pos_index;
    Vec3b pos_val2;
    vector<Vec3b> pos_val_index;
    for(int i=pading;i<img_mat.rows-pading;i++)
    {
        for(int j=pading;j<img_mat.cols-pading;j++)
        {
            if(img_mat.at<Vec3b>(i,j) == pix_val){
                pos.x = j;
                pos.y = i;
                pos_index.push_back(pos);

            }
        }
    }
    for(int i=0;i<pos_index.size();i++)
    {
        pos_val2 = convolutioncalcullatepix(img_mat,pos_index[i],pix_val,threshold);
        pos_val_index.push_back(pos_val2);
    }

    for(int i=0;i<pos_index.size();i++){
        img_mat.at<Vec3b>(pos_index[i].y,pos_index[i].x) = pos_val_index[i];

    }
}
int main(int argv, char **argc)
{
    char path[128] = "/home/iscreate/code/pic_deal_pix/save 2.png";
    Mat img_mat = imread(path);


    vector<Vec3b> type_list_index;
    //获取颜色列表
    type_list_index = colorlist();
    //cout<<"type_list_index = "<<type_list_index.size()<<endl;

    //将图中颜色不是颜色列表的点变成黑色
    Vec3b black_val = Vec3b(0,0,0);
    otherpixval2intendpixval(img_mat,type_list_index,black_val);

    imshow("img_mat1",img_mat);
    imwrite("img_mat_withe.png",img_mat);
    waitKey(0);

    //找到黑色像素点的位置并将他变成卷积核中颜色最多的点的颜色
    removediscretedot(img_mat,black_val,threshold_val,con_kernel_size);

    imshow("img_mat",img_mat);
    imwrite("img_mat_black.png",img_mat);
    waitKey(0);

    return 0;
}


