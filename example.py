import iksk

iksk_instance = iksk.iksk()
result = iksk_instance.encrypt('Hello World', mode=[0, 1, 2, 3, 1])
print('加密后内容 :'+result[0])
print('解密后内容:'+iksk_instance.decrypt(result[0], mode=[0, 1, 2, 3, 1], sn=result[1]))
