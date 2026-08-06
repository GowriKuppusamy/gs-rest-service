package com.example.restservice;

import static org.assertj.core.api.Assertions.assertThat;
import org.junit.jupiter.api.Test;

import com.example.restservice.service.GreetingService;

class GreetingControllerTest {

  private final GreetingService greetingService = new GreetingService();

  @Test
  void returnsDefaultGreetingWhenNameIsNotProvided() {
    assertThat(greetingService.greet(null)).isEqualTo("Hello, World!");
  }

  @Test
  void returnsPersonalizedGreetingWhenNameIsProvided() {
    assertThat(greetingService.greet("Alice")).isEqualTo("Hello, Alice!");
  }
}
