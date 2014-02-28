figure(1)

hold on
imshow(trainitems(index).origimage)
HEIGHT = 360;
WIDTH = 640;
M = ROWS;
N = COLS;
x = 1;
y = 1;
w = HEIGHT/N;
h = WIDTH/M;
for r = 1:M
    for c = 1:N
        rectangle('Position',[x,y,h,w],'EdgeColor','b','LineWidth',1)
        hold on
        plot(trainitems(index).centerx,trainitems(index).centery,'r.','MarkerSize',20)
        y = c*w;
    end
    x = r*h;
    y = 1;
end
title('Image Sector Example')
