"""Main module for basic command-line usage."""
from .mouse import get_sys_power_supply_mice


def main():  # pragma: no cover
    """Main function."""
    for mouse in get_sys_power_supply_mice():
        print(f'{mouse.model}: {mouse.percentage}/{mouse.status.value}')


if __name__ == '__main__':  # pragma: no cover
    main()
