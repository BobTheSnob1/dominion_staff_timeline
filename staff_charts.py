def main():
    print("Select the chart you want to generate:")
    print("1. Team Size Over Time by Role")
    print("2. Duration in Staff Roles per Member")
    print("3. Staff Timeline")
    print("Enter the number corresponding to your choice, or 'exit' to quit:")

    choice = input().strip().lower()

    if choice == '1':
        import team_size_over_time
        team_size_over_time.plot_team_size_over_time()
    elif choice == '2':
        import staff_roles_duration
        staff_roles_duration.plot_staff_roles_duration()
    elif choice == '3':
        import staff_timeline
        staff_timeline.plot_staff_timeline()
    elif choice == 'exit':
        return
    else:
        print("Invalid input. Please try again.")
        main()


if __name__ == "__main__":
    main()
