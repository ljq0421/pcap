package org.fkjava.mavenqs;
import org.apache.tomcat.jni.Proc;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Service;
import javax.websocket.*;
import javax.websocket.server.ServerEndpoint;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.concurrent.CopyOnWriteArraySet;

@Service
@ServerEndpoint(value = "/showrule")
@Component

public class Ruleshow {
    //concurrent包的线程安全Set，用来存放每个客户端对应的MyWebSocket对象。
    private static CopyOnWriteArraySet<Ruleshow> webSocketSet = new CopyOnWriteArraySet<Ruleshow>();

    //与某个客户端的连接会话，需要通过它来给客户端发送数据
    private Session session;

    /**
     * 连接建立成功调用的方法*/
    @OnOpen
    public void onOpen(Session session) throws IOException {
        this.session = session;
        webSocketSet.add(this);     //加入set中
        Process process=Runtime.getRuntime().exec("python /root/pcap/showrule.py");
        System.out.println("python /root/pcap/showrule.py");
        String line=null;
        InputStream is = process.getInputStream();
        InputStreamReader isr = new InputStreamReader(is);
        BufferedReader br = new BufferedReader(isr);
        while ((line = br.readLine()) != null) {
            System.out.println(line);
            System.out.flush();
            sendMessage(line);
        }
        isr.close();
        br.close();
        is.close();
    }

    /**
     * 连接关闭调用的方法
     */
    @OnClose
    public void onClose() {
        webSocketSet.remove(this);  //从set中删除
    }

    public void sendMessage(String message) throws IOException {
        this.session.getBasicRemote().sendText(message);
    }


}


