def java_convert(js):

  img_java = b64decode(js.split(',')[1])
  img_np = np.frombuffer(img_java, dtype=np.uint8)
  img = cv2.imdecode(img_np, flags=1)

  return img