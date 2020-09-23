import os


if os.path.exists('./webapp/bpp'):
    cwd = os.getcwd()
    os.chdir(os.path.join(cwd, 'webapp'))
    os.system('yarn webpack:prod')
    os.chdir(cwd)
