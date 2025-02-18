import chalk from 'chalk';
import clear from 'clear';
import figlet from 'figlet';
import gradient from 'gradient-string';
import { createRequire } from 'module';
const require = createRequire(import.meta.url);

class AIAssistantSimulation {
    constructor() {
        this.commands = [
            "Turn on the green LED",
            "Blink the red LED three times",
            "Turn both LEDs on",
            "Turn everything off",
            "Make the green LED pulse"
        ];
        this.ledStates = { red: false, green: false };
    }

    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    drawFrame(aiState, command, thinkingDots = "") {
        clear();
        
        // Title with gradient
        console.log(gradient.pastel.multiline(figlet.textSync('AI LED', {
            font: 'Small',
            horizontalLayout: 'fitted'
        })));

        // LED states
        const redLed = this.ledStates.red ? chalk.red('●') : chalk.gray('○');
        const greenLed = this.ledStates.green ? chalk.green('●') : chalk.gray('○');

        console.log(`
    ╔══════════════════════════════════════════════╗
    ║             AI LED ASSISTANT                 ║
    ╚══════════════════════════════════════════════╝

         [RED]${redLed}      [GREEN]${greenLed}
    
         ┌─────────────┐
         │  ${chalk.cyan(aiState.padStart(6).padEnd(11))} │
         └─────────────┘
                │
                ▼
    ${chalk.yellow(`Command: ${command}${thinkingDots}`)}
        `);
    }

    async animateThinking(command) {
        const dots = [".", "..", "...", "...."];
        for (let i = 0; i < 8; i++) {
            for (const dot of dots) {
                this.drawFrame("THINKING", command, dot);
                await this.sleep(200);
            }
        }
    }

    async animateProcessing(command, steps) {
        for (const [state, leds] of steps) {
            this.ledStates = leds;
            this.drawFrame(state, command);
            await this.sleep(800);
        }
    }

    async runSimulation() {
        try {
            while (true) {
                // Reset state
                this.ledStates = { red: false, green: false };
                
                // Choose random command
                const command = this.commands[Math.floor(Math.random() * this.commands.length)];
                
                // Listening state
                this.drawFrame("LISTENING", "");
                await this.sleep(1000);
                
                // Show command and think
                await this.animateThinking(command);
                
                // Process command with appropriate animations
                switch (command) {
                    case "Turn on the green LED":
                        await this.animateProcessing(command, [
                            ["PROCESSING", { red: false, green: false }],
                            ["EXECUTING", { red: false, green: true }],
                            ["COMPLETED", { red: false, green: true }]
                        ]);
                        break;
                        
                    case "Blink the red LED three times":
                        for (let i = 0; i < 3; i++) {
                            this.ledStates.red = true;
                            this.drawFrame("BLINKING", command);
                            await this.sleep(500);
                            this.ledStates.red = false;
                            this.drawFrame("BLINKING", command);
                            await this.sleep(500);
                        }
                        break;
                        
                    case "Turn both LEDs on":
                        await this.animateProcessing(command, [
                            ["PROCESSING", { red: false, green: false }],
                            ["EXECUTING", { red: true, green: false }],
                            ["EXECUTING", { red: true, green: true }],
                            ["COMPLETED", { red: true, green: true }]
                        ]);
                        break;
                        
                    case "Turn everything off":
                        await this.animateProcessing(command, [
                            ["PROCESSING", { red: true, green: true }],
                            ["EXECUTING", { red: false, green: true }],
                            ["EXECUTING", { red: false, green: false }],
                            ["COMPLETED", { red: false, green: false }]
                        ]);
                        break;
                        
                    case "Make the green LED pulse":
                        for (let i = 0; i < 4; i++) {
                            this.ledStates.green = true;
                            this.drawFrame("PULSING", command);
                            await this.sleep(300);
                            this.ledStates.green = false;
                            this.drawFrame("PULSING", command);
                            await this.sleep(300);
                        }
                        break;
                }
                
                // Wait before next command
                await this.sleep(2000);
            }
        } catch (error) {
            clear();
            console.log("\nSimulation ended. Thank you for watching!");
        }
    }
}

// Create and run the simulation
const simulation = new AIAssistantSimulation();
simulation.runSimulation();