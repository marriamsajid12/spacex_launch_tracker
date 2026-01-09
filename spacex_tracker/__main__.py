from datetime import datetime
from typing import List, Optional
from spacex_tracker.launch import LaunchService
from spacex_tracker.stats import (
    success_rate_by_rocket,
    launches_per_site,
    launch_frequency_monthly,
    launch_frequency_yearly
)


def parse_date(date: str) -> Optional[datetime]:
    """Parse user input date in YYYY-MM-DD format"""
    if not date:
        return None
    try:
        return datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print(f"Invalid date format: '{date}'. Use YYYY-MM-DD.")
        return None


def print_launches(launches: List) -> None:
    """Print key details of launches"""
    if not launches:
        print("No launches to display.")
        return

    print("\n--- Launch Details ---")
    for i, launch in enumerate(launches, start=1):
        print(
            f"{i}. Name: {launch.name}, Date: {launch.date_utc.strftime('%Y-%m-%d')}, "
            f"Rocket: {launch.rocket}, Success: {launch.success}, Launchpad: {launch.launchpad}"
        )


def main() -> None:
    service = LaunchService()

    # Fetch launches
    try:
        launches = service.get_launches()
        print(f"Total launches fetched: {len(launches)}\n")
    except Exception as e:
        print(f"Error fetching launches: {e}")
        return

    #print_launches(launches)

    # Interactive filtering loop
    while True:
        filtered_launches = launches[:]

        print("\nFilter options:")
        print("1. Date range")
        print("2. Rocket name")
        print("3. Rocket type")
        print("4. Launch success/failure")
        print("5. Launch site")
        print("6. Show all launches")
        print("7. Show statistics")
        print("0. Exit")
        choice = input("Choose a filter option: ").strip()

        if choice == "1":
            start = parse_date(input("Start date (YYYY-MM-DD): ").strip())
            end = parse_date(input("End date (YYYY-MM-DD): ").strip())

            if start is None and end is None:
                print("No valid dates provided. Filter cancelled.")
                continue

            if start and end and start > end:
                print("Start date must be before end date. Filter cancelled.")
                continue

            filtered_launches = service.filter_launches(filtered_launches, start_date=start, end_date=end)
            print(f"\nFiltered launches count: {len(filtered_launches)}")
            print_launches(filtered_launches)


        elif choice == "2":
            name = input("Rocket name: ").strip()
            if name:
                filtered_launches = service.filter_launches(filtered_launches, name=name)
                print(f"\nFiltered launches count: {len(filtered_launches)}")
                print_launches(filtered_launches)

        elif choice == "3":
            rocket = input("Rocket type: ").strip()
            if rocket:
                filtered_launches = service.filter_launches(filtered_launches, rocket=rocket)
                print(f"\nFiltered launches count: {len(filtered_launches)}")
                print_launches(filtered_launches)

        elif choice == "4":
            success_input = input("Launch success? (yes/no): ").strip().lower()
            if success_input == "yes":
                filtered_launches = service.filter_launches(filtered_launches, success=True)
            elif success_input == "no":
                filtered_launches = service.filter_launches(filtered_launches, success=False)
            print(f"\nFiltered launches count: {len(filtered_launches)}")
            print_launches(filtered_launches)

        elif choice == "5":
            launchpad = input("Launch site name: ").strip()
            if launchpad:
                filtered_launches = service.filter_launches(filtered_launches, launchpad=launchpad)
                print(f"\nFiltered launches count: {len(filtered_launches)}")
                print_launches(filtered_launches)

        elif choice == "6":
            print_launches(launches)

        elif choice == "7":
            try:
                print("\nSuccess rate by rocket:")
                rates = success_rate_by_rocket(filtered_launches)
                for rocket_name, rate in rates.items():
                    print(f"{rocket_name}: {rate:.2%}")
            except Exception as e:
                print(f"Error calculating success rates: {e}")

            try:
                print("\nLaunches per site:")
                site_counts = launches_per_site(filtered_launches)
                for site, count in site_counts.items():
                    print(f"{site}: {count}")
            except Exception as e:
                print(f"Error calculating launches per site: {e}")

            try:
                monthly = launch_frequency_monthly(launches)
                yearly = launch_frequency_yearly(launches)

                print("\nMonthly launch frequency:")
                for period, count in monthly.items():
                    print(f"{period}: {count}")

                print("\nYearly launch frequency:")
                for year, count in yearly.items():
                    print(f"{year}: {count}")

            except Exception as e:
                print(f"Error calculating launch frequency: {e}")

        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
