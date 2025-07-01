from deploy import main

try:
    main()
except KeyboardInterrupt:
    print("Canceled")
