package com.example;

import net.fabricmc.api.ClientModInitializer;
import net.minecraft.client.MinecraftClient;
import net.minecraft.client.option.GameOptions;
import net.minecraft.entity.effect.StatusEffectInstance;
import net.minecraft.entity.effect.StatusEffects;

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

public class ExampleModClient implements ClientModInitializer {
	private static final Logger LOGGER = LogManager.getLogger("ExampleMod");
	private static final Path SETTINGS_FILE = Paths.get(System.getProperty("user.home"), "minecraft-accessibility-settings.txt");

	@Override
	public void onInitializeClient() {
		LOGGER.info("Starting MOD client");

        // Start a thread to watch for brightness triggers
       Thread watcher = new Thread(() -> {
            try {
                while (true) {
                    if (Files.exists(SETTINGS_FILE)) {
                        List<String> lines = Files.readAllLines(SETTINGS_FILE);
                        Map<String, String> settings = new HashMap<>();
                        for (String line : lines) {
                          String[] parts = line.split("=", 2);
                          if (parts.length == 2) {
                              settings.put(parts[0].trim().toLowerCase(), parts[1].trim().toLowerCase());
                          }
                         }
                        
												MinecraftClient client = MinecraftClient.getInstance();
                        if ("on".equals(settings.get("brightness_mode"))) {
                            client.execute(() -> {
                                setGamma(client, 1.0F);
                                applyNightVision(client);
                            });
                        } else if ("off".equals(settings.get("brightness_mode"))) {
							client.execute(() -> {
								setGamma(client, 0.2F);
							});
                        }

                        if ("on".equals(settings.get("zoom_out"))) {
                            client.execute(() -> setFOV(client, 100.0)); // Higher FOV, zoom out
                        } else if ("off".equals(settings.get("zoom_out"))) {
                            client.execute(() -> setFOV(client, 70.0)); // Default FOV
                        }

                    }
                    Thread.sleep(1000); // check every second
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        });

				watcher.setDaemon(true);
				watcher.start();
	}

	private void applyNightVision(MinecraftClient client) {
		if (client.player != null) {
            client.player.addStatusEffect(
                new StatusEffectInstance(StatusEffects.NIGHT_VISION, 220, 0, false, false)
            );
        }
	}

	private void setGamma(MinecraftClient client, double value) {
        if (client != null && client.options != null) {
            GameOptions options = client.options;

            // Clamp value to Minecraft's valid range (0.0 to 1.0)
            double clamped = Math.max(0.0, Math.min(1.0, value));
            options.getGamma().setValue(clamped);

            System.out.println("Set gamma to " + clamped);
            LOGGER.info("Set gamma to " + clamped);
        }
    }

    private void setFOV(MinecraftClient client, double value) {
    if (client != null && client.options != null) {
        // Clamp to Minecraft's typical FOV range (30–110)
        double clamped = Math.max(30.0, Math.min(110.0, value));
        client.options.getFov().setValue((int) clamped);

        System.out.println("Set FOV to " + clamped);
        LOGGER.info("Set FOV to " + clamped);
    }
}
}