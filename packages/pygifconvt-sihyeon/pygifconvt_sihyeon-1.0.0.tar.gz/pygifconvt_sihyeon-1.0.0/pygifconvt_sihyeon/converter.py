import glob
from PIL import Image

class GifConverter:
    def __init__(self, path_in=None, path_out=None, resize=(320, 240)):
        '''
        path_in : 원본 여러 이미지 경로(Ex : images/*.png)
        path_out : 결과 이미지 경로 (Ex : output/filename.gif)
        resize : 리사이징 크기(320, 240)
        '''
        self._path_in = path_in or './*.png'
        self._path_out = path_out or './output.gif'
        self._resize = resize

    def convert_gif(self):
        '''
        GIF 이미지 변환 기능 수행

        '''
        print(self._path_in, self._path_out, self._resize)
        
        img, *images = \
            [Image.open(f).resize(self._resize, Image.ANTIALIAS) for f in sorted(glob.glob(self._path_in))]

        try :
            img.save(
                fp=self._path_out,
                format = 'GIF',
                append_images = images,
                save_all = True,
                duration = 1000, #  클수록 느리게 전환
                loop = 0,
            )
        except IOError:
            print('Cannot convert!', img)


if __name__ == '__main__':
    # 클래스 선언
    c = GifConverter('./project/images/*.png','./project/image_out/result.gif')
    # 변환
    c.convert_gif()