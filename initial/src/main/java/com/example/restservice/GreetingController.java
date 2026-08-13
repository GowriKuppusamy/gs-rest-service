package com.example.restservice;

import java.util.concurrent.atomic.AtomicLong;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class GreetingController {

  private static final String template = "Hello, %s!";
  private final AtomicLong counter = new AtomicLong();

  @GetMapping("/greeting")
  public Greeting greeting(@RequestParam(required = false) String name) {
    String effectiveName = resolveName(name);
    return new Greeting(counter.incrementAndGet(), template.formatted(effectiveName));
  }

  private static String resolveName(String name) {
    if (name == null || name.isBlank()) {
      return "World";
    }
    return name;
  }
}
