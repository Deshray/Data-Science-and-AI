import turtle

def koch_snowflake(turtle, order, size):
    if order == 0:
        turtle.forward(size)
    else:
        for angle in [60, -120, 60, 0]:
            koch_snowflake(turtle, order-1, size/3)
            turtle.left(angle)

def draw_koch_snowflake(order, size):
    screen = turtle.Screen()
    screen.bgcolor("white")
    
    snowflake_turtle = turtle.Turtle()
    snowflake_turtle.speed(2)
    
    for _ in range(3):
        koch_snowflake(snowflake_turtle, order, size)
        snowflake_turtle.right(120)
    
    screen.exitonclick()

if __name__ == "__main__":
    order = int(input("Enter the order of the Koch snowflake: "))
    size = int(input("Enter the size of the Koch snowflake: "))
    
    draw_koch_snowflake(order, size)
