package com.crio.starter.data;

import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.MongoId;

@Data
@Document(collection = "messages")
@NoArgsConstructor
public class GreetingsEntity {

  @MongoId
  private String id;

  private String message;

}
