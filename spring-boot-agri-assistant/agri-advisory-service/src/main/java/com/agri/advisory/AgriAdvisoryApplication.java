package com.agri.advisory;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Entry point for the Agri Advisory Microservice (port 8081).
 * Starts the Spring context that hosts the REST API + embedded backend.
 */
@SpringBootApplication
public class AgriAdvisoryApplication {

    public static void main(String[] args) {
        SpringApplication.run(AgriAdvisoryApplication.class, args);
    }
}
