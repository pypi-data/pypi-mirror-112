# Copernic360 command-line tool

The copernic360 command-line wraps Kagenova's Copernic360 CLI. In short, it
allows users to post 360 images and videos and get Copernic360 configuration
files back.

Users first need an account with Kagenova's
[Copernic360](https://kagenova.com/products/copernic360/) product. After
installing the tool via [pip](https://pypi.org/project/copernic360_cli), users
can interact with the Copernic360 API as follows:

```bash
# get help
copernic360 --help
# check user login
copernic350 check-login
# check user's credits
copernic350 check-credit
# uploaad image.jpg and get its configution back (config.6dof)
copernic360 process-content image.jpg config.6dof
```

See the command-line help for futher functionality and parameters.