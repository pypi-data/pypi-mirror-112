"""main entry for ekea command-line interface"""


def main():
    from ekea import E3SMKea
    ret, _ = E3SMKea().run_command()
    return ret


if __name__ == "__main__":
    main()
