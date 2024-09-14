import iksk

iksk_instance = iksk.iksk()
result = iksk_instance.encrypt('Hello World', mode=[0, 1, 2, 3, 1])
print('加密后内容 :'+result)
print('解密后内容'+iksk_instance.decrypt(result_mode0[0], mode=[0, 1, 2, 3, 1], sn=result_mode0[1]))
