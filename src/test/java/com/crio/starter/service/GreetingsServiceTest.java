package com.crio.starter.service;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.crio.starter.data.GreetingsEntity;
import com.crio.starter.exchange.ResponseDto;
import com.crio.starter.repository.GreetingsRepository;
import java.util.Optional;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class GreetingsServiceTest {

  @Mock
  private GreetingsRepository greetingsRepository;

  @InjectMocks
  private GreetingsService greetingsService;

  @Test
  void getMessage() {
    GreetingsEntity greetingsEntity = getGreeting("001", "Welcome");
    Mockito.doReturn(greetingsEntity)
        .when(greetingsRepository).findByExtId("001");
    ResponseDto responseDto = greetingsService.getMessage("001");

    ResponseDto expected = new ResponseDto("Welcome");
    assertEquals(expected, responseDto);

  }

  private GreetingsEntity getGreeting(String id, String message) {
    GreetingsEntity greetingsEntity = new GreetingsEntity();
    greetingsEntity.setExtId(id);
    greetingsEntity.setMessage(message);
    return greetingsEntity;
  }
}