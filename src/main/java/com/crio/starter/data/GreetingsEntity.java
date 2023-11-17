package com.crio.starter.data;

import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document(collection = "greetings")
@NoArgsConstructor
public class GreetingsEntity {

  private String extId;

  private String message;

}
