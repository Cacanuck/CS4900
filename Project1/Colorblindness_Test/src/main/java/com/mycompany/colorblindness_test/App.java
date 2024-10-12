package com.mycompany.colorblindness_test;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.scene.shape.Rectangle;
import javafx.stage.Stage;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.time.Duration;
import java.time.LocalDateTime;
import java.awt.AWTException;
import java.awt.Robot; //

public class App extends Application {

    private final List<Color> inputColors1 = new ArrayList<>();
    private final List<Color> inputColors2 = new ArrayList<>();
    private List<Button> colorButtons;
    private Rectangle centralColorBox;
    private Stage primaryStage;
    private Scene initialScene;
    private Map<Button, Color> buttonColorMap = new HashMap<>();
    private Map<Color, String> colorNames = new HashMap<>();
    private List<Color> currentInputColors;
    private LocalDateTime startTime;

    @Override
    public void start(Stage stage) {
        primaryStage = stage;
        primaryStage.setTitle("Color Picker App");

        // Original colors
        inputColors1.add(Color.web("#ff0000")); // Red
        inputColors1.add(Color.web("#7f6000")); // Brown
        inputColors1.add(Color.web("#385723")); // Green
        inputColors1.add(Color.web("#ffff00")); // Yellow
        inputColors1.add(Color.web("#002f8e")); // Blue
        inputColors1.add(Color.web("#7030a0")); // Purple

        // New colors
        inputColors2.add(Color.web("#ff9898")); // New Red
        inputColors2.add(Color.web("#541f00")); // New Brown
        inputColors2.add(Color.web("#92D050")); // New Green
        inputColors2.add(Color.web("#ffff00")); // New Yellow
        inputColors2.add(Color.web("#00f1ff")); // New Blue
        inputColors2.add(Color.web("#5a238e")); // New Purple

        // Initialize color names
        colorNames.put(Color.web("#ff0000"), "Red");
        colorNames.put(Color.web("#7f6000"), "Brown");
        colorNames.put(Color.web("#385723"), "Green");
        colorNames.put(Color.web("#ffff00"), "Yellow");
        colorNames.put(Color.web("#002f8e"), "Blue");
        colorNames.put(Color.web("#7030a0"), "Purple");

        colorNames.put(Color.web("#ff9898"), "Red");
        colorNames.put(Color.web("#541f00"), "Brown");
        colorNames.put(Color.web("#92D050"), "Green");
        colorNames.put(Color.web("#00f1ff"), "Blue");
        colorNames.put(Color.web("#5a238e"), "Purple");

        Button button1 = new Button("Open Color Picker 1");
        Button button2 = new Button("Open Color Picker 2");

        button1.setOnAction(e -> {
            System.out.println("Original Color Test");
            showColorPickerScene("Color Picker 1", inputColors1);
            try { //
                int xCoord = 760; //
                int yCoord = 400; //
                Robot robot = new Robot(); //
                robot.mouseMove(xCoord, yCoord); //
            } catch (AWTException o) { //
            } //
        });
        button2.setOnAction(e -> {
            System.out.println("New Color Test");
            showColorPickerScene("Color Picker 2", inputColors2);
            try { //
                int xCoord = 760; //
                int yCoord = 400; //
                Robot robot = new Robot(); //
                robot.mouseMove(xCoord, yCoord); //
            } catch (AWTException o) { //
            } //
        });

        VBox vbox = new VBox(10, button1, button2);
        vbox.setStyle("-fx-padding: 20;");

        initialScene = new Scene(vbox, 300, 200);
        primaryStage.setScene(initialScene);
        primaryStage.show();
    }

    private void showColorPickerScene(String title, List<Color> colors) {
        // Set the current input colors
        currentInputColors = colors;

        centralColorBox = new Rectangle(100, 100);
        centralColorBox.setStyle("-fx-border-color: black;");

        GridPane surroundingPane = new GridPane();
        surroundingPane.setHgap(10);
        surroundingPane.setVgap(10);

        colorButtons = new ArrayList<>();
        buttonColorMap.clear();

        for (int i = 0; i < 6; i++) {
            Button colorButton = new Button();
            colorButton.setStyle(
                    "-fx-pref-width: 50; -fx-pref-height: 50; -fx-min-width: 50; -fx-min-height: 50; -fx-max-width: 50; -fx-max-height: 50;");
            colorButton.setMinSize(50, 50);
            colorButton.setMaxSize(50, 50);
            colorButton.setOnAction(e -> handleColorButtonClick(colorButton));
            colorButtons.add(colorButton);
            surroundingPane.add(colorButton, i % 2, i / 2);

            if (i == 0) { //
                colorButton.setTranslateX(50); //
                colorButton.setTranslateY(-100); //
            } else if (i == 1) { //
                colorButton.setTranslateX(182); //
                colorButton.setTranslateY(-100); //
            } else if (i == 2) { //
                colorButton.setTranslateX(20); //
                colorButton.setTranslateY(-60); //
            } else if (i == 3) { //
                colorButton.setTranslateX(215); //
                colorButton.setTranslateY(-60); //
            } else if (i == 4) { //
                colorButton.setTranslateX(50); //
                colorButton.setTranslateY(-25); //
            } else { //
                colorButton.setTranslateX(182); //
                colorButton.setTranslateY(-25); //
            } //
        }

        // Back Button
        Button backButton = new Button("Back");
        backButton.setOnAction(e -> primaryStage.setScene(initialScene));

        VBox vbox = new VBox(10, centralColorBox, surroundingPane, backButton);
        vbox.setStyle("-fx-padding: 20;");

        centralColorBox.setTranslateX(122); //
        centralColorBox.setTranslateY(85); //

        Scene colorPickerScene = new Scene(vbox, 400, 350);
        primaryStage.setScene(colorPickerScene);

        // Initial randomization
        randomizeColors();
    }

    private void handleColorButtonClick(Button clickedButton) {
        Color centralColor = (Color) centralColorBox.getFill();
        Color buttonColor = buttonColorMap.get(clickedButton);
        String centralColorName = colorNames.get(centralColor);
        String buttonColorName = colorNames.get(buttonColor);

        // Calculate the time for each selection
        LocalDateTime currentTime = LocalDateTime.now();
        Duration duration = Duration.between(startTime, currentTime);
        double elapsedTimeSeconds = duration.toMillis() / 1000.0;

        // Format the elapsed time to 2 decimal places
        String formattedElapsedTime = String.format("%.2f", elapsedTimeSeconds);

        System.out.println("Central Color: " + centralColorName +
                " | Picked Color: " + buttonColorName +
                " | Time Elapsed: " + formattedElapsedTime + " seconds");

        try { //
            int xCoord = 760; //
            int yCoord = 400; //
            Robot robot = new Robot(); //
            robot.mouseMove(xCoord, yCoord); //
        } catch (AWTException o) { //
        } //

        // Re-randomize colors when a button is clicked
        randomizeColors();
    }

    private void randomizeColors() {

        // Initialize the timer
        startTime = LocalDateTime.now();

        // Create a list of colors and shuffle it
        List<Color> colors = new ArrayList<>(currentInputColors);
        Collections.shuffle(colors);

        // Set the central color
        if (centralColorBox != null) {
            // Pick a color from the shuffled list for the central color
            Color centralColor = colors.get(0);
            centralColorBox.setFill(centralColor);

            // Remove the central color from the list
            colors.remove(0);
        }

        // Set the surrounding colors
        if (colorButtons != null) {
            // Add the central color to the list of surrounding colors
            Color centralColor = (Color) centralColorBox.getFill();
            colors.add(centralColor);
            Collections.shuffle(colors);

            for (int i = 0; i < colorButtons.size(); i++) {
                Button colorButton = colorButtons.get(i);
                Color color = colors.get(i);
                colorButton.setStyle(
                        "-fx-background-color: #" + toHexString(color) + "; -fx-pref-width: 50; -fx-pref-height: 50;");
                buttonColorMap.put(colorButton, color);
            }
        }
    }

    private String toHexString(Color color) {
        return String.format("%02X%02X%02X", (int) (color.getRed() * 255),
                (int) (color.getGreen() * 255),
                (int) (color.getBlue() * 255));
    }

    public static void main(String[] args) {
        launch(args);
    }
}
