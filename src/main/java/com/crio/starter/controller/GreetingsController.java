package com.crio.starter.controller;

import com.crio.starter.exchange.ResponseDto;
import com.crio.starter.service.GreetingsService;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor(onConstructor = @__(@Autowired))
public class GreetingsController {

  private final GreetingsService greetingsService;

  @GetMapping("/say-hello")
  public ResponseDto sayHello(@RequestParam String messageId) {
    return greetingsService.getMessage(messageId);
  }

}
