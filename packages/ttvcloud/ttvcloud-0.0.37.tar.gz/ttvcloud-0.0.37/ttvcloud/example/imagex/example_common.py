# coding:utf-8
from __future__ import print_function
from ttvcloud.imagex.ImageXService import ImageXService

if __name__ == '__main__':
    imagex_service = ImageXService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    imagex_service.set_ak('AKLTMDRhMGQ1ZWE4NjZkNDg0ZGJmMjg5OTUzNzU4NzRmOWM')
    imagex_service.set_sk('u4zCNZS9bFjqNjaazTASYgkNUfk9vM/i2rp8zXzTjHN64YoU+/wx+iJfZv5LUt9B')

    params = dict()
    params['ServiceId'] = 'su4pp6x6rv'
    params['StoreUri'] = '0e88cb509813ad87305b4558698a3296.jpg'

    resp = imagex_service.imagex_get('GetImageUploadFile', params)
    print(resp)