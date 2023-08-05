import insightface_paddle as face
import logging
logging.basicConfig(level=logging.INFO)


# Get help
try:
    parser = face.parser()
    help_info = parser.print_help()
    print(help_info)
except Exception as e:
    print(e)

# Building base lib
try:
    parser = face.parser()
    args = parser.parse_args()
    args.build_index = "./demo/friends/index.bin"
    args.img_dir = "./demo/friends/gallery"
    args.label = "./demo/friends/gallery/label.txt"
    predictor = face.InsightFace(args)
    predictor.build_index()
except Exception as e:
    print(e)
    # exit()

# Detection only
try:
    parser = face.parser()
    args = parser.parse_args()

    args.det = True
    args.output = "./demo/friends/output"
    input_path = "./demo/friends/query/friends1.jpg"

    predictor = face.InsightFace(args)
    res = predictor.predict(input_path)
    print(next(res))
except Exception as e:
    print(e)

try:
    parser = face.parser()
    args = parser.parse_args()
    args.det = True
    args.output = "./demo/friends/output"
    predictor = face.InsightFace(args)
    path = "./demo/friends/query/friends1.jpg"
    import cv2
    img = cv2.imread(path)
    res = predictor.predict(img)
    print(next(res))
except Exception as e:
    print(e)

try:
    parser = face.parser()
    args = parser.parse_args()
    args.det = True
    args.output = "./demo/friends/output"
    predictor = face.InsightFace(args)
    input_path = "./demo/friends/query/friends.mp4"
    res = predictor.predict(input_path)
    for _ in res:
        print(_)
except Exception as e:
    print(e)

# Recognition only
try:
    parser = face.parser()
    args = parser.parse_args()
    args.rec = True
    args.index = "./demo/friends/index.bin"
    predictor = face.InsightFace(args)
    input_path = "./demo/friends/query/Rachel.png"
    res = predictor.predict(input_path, print_info=True)
    next(res)
except Exception as e:
    print(e)

try:
    parser = face.parser()
    args = parser.parse_args()
    args.rec = True
    args.index = "./demo/friends/index.bin"
    predictor = face.InsightFace(args)
    path = "./demo/friends/query/Rachel.png"
    import cv2
    img = cv2.imread(path)
    res = predictor.predict(img, print_info=True)
    next(res)
except Exception as e:
    print(e)

# Detection and recognition
try:
    parser = face.parser()
    args = parser.parse_args()
    args.det = True
    args.rec = True
    args.index = "./demo/friends/index.bin"
    args.output = "./demo/friends/output"
    predictor = face.InsightFace(args)
    input_path = "./demo/friends/query/friends1.jpg"
    res = predictor.predict(input_path, print_info=True)
    next(res)
except Exception as e:
    print(e)

try:
    parser = face.parser()
    args = parser.parse_args()
    args.det = True
    args.rec = True
    args.index = "./demo/friends/index.bin"
    args.output = "./demo/friends/output"
    predictor = face.InsightFace(args)
    path = "./demo/friends/query/friends1.jpg"
    import cv2
    img = cv2.imread(path)
    res = predictor.predict(img, print_info=True)
    next(res)
except Exception as e:
    print(e)

try:
    parser = face.parser()
    args = parser.parse_args()
    args.det = True
    args.rec = True
    args.index = "./demo/friends/index.bin"
    args.output = "./demo/friends/output"
    predictor = face.InsightFace(args)
    input_path = "./demo/friends/query/friends.mp4"
    res = predictor.predict(input_path, print_info=True)
    for _ in res:
        pass
except Exception as e:
    print(e)
